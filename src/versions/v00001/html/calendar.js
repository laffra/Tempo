var currentDate = new Date(new Date().getFullYear(), new Date().getMonth());

function render() {
  var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  $('#month').text(months[currentDate.getMonth()] + " " + currentDate.getFullYear());
  renderGrid();
  renderEvents();
}

function parseEvents(events) {
  var eventMap = { };
  var max = 0;
  for (var n = 0; n < events.length; n++) {
    var event = events[n];
    var timestamp = event[0];
    var date = new Date(timestamp * 1000);
    var weekIndex = Math.floor(date.getDate() / 7);
    var dayIndex = date.getDay();
    var key = "" + weekIndex + dayIndex;
    if (!eventMap[key]) {
      eventMap[key] = [];
      for (var n = 0; n < 24; n++) {
        eventMap[key].push(0);
      }
    }
    max = Math.max(eventMap[key][date.getHours()]++, max);
  }
  eventMap["max"] = max;
  return eventMap;
}

function renderEvents() {
  var start = currentDate.getTime()/1000;
  var end = start + 60 * 60 * 24 * 31;
  $.get("http://localhost:1187/events?start=" + start + "&end=" + end, function(events) {
    var eventMap = parseEvents(events);
    for (var key in eventMap) {
      var hours = $("<div>");
      for (var n = 0; n < 24; n++) {
        var color = 256 - Math.min(256, Math.floor(256 * eventMap[key][n] / 1800));
        var hour = $("<div>")
          .addClass("hour")
          .css("background-color", "rgb("+color+","+color+","+color+")")
        hours.append(hour);
      }
      $("#cell" + key)
        .find(".number")
        .append(hours);
    }
  })
}

function renderGrid() {
  $(".current").removeClass("current");
  $(".number").text("");
  var weekIndex = 0;
  var month = currentDate.getMonth();
  var date = new Date(currentDate.getFullYear(), month);
  $(".week").css("display", "none");
  for (var day = 1; day < 32; day++) {
    date.setDate(day);
    var dayIndex = date.getDay();
    if (date.getMonth() == month) {
      $("#cell" + weekIndex + dayIndex)
        .addClass("current")
        .find(".number")
        .text(day);
      $("#week" + weekIndex)
        .css("display", "table-row");
    }
    if (dayIndex == 6) {
      weekIndex++;
    }
  }
}

$("#back").click(function() {
  currentDate.setMonth(currentDate.getMonth() - 1);
  render();
});

$("td").click(function() {
  if (!$(this).find(".number").text()) {
    var diff = $(this).parent().attr("id") == "week0" ? -1 : 1;
    currentDate.setMonth(currentDate.getMonth() + diff);
    render();
  }
});

$("#forward").click(function() {
  currentDate.setMonth(currentDate.getMonth() + 1);
  render();
});

render();
