var currentDate = new Date(new Date().getFullYear(), new Date().getMonth());

var INDEX_TIMESTAMP = 0;
var INDEX_SYSTEM = 1;
var INDEX_CPU = 2;
var INDEX_USER = 3;
var INDEX_PID = 4;
var INDEX_PPID = 5;
var INDEX_APP_NAME = 6;
var INDEX_TITLE = 7;
var INDEX_FAV = 8;
var INDEX_URL = 9;

var MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function render() {
  console.log(new Date(), "render");
  $('#month').text(MONTH_NAMES[currentDate.getMonth()] + " " + currentDate.getFullYear());
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
        eventMap[key].push([]);
      }
    }
    var hours = date.getHours();
    eventMap[key][hours].push(event);
    max = Math.max(eventMap[key][hours].length, max);
  }
  eventMap["max"] = max;
  return eventMap;
}

function renderEvents() {
  var start = currentDate.getTime()/1000;
  var end = start + 60 * 60 * 24 * 31;
  $.get("http://localhost:1187/events?start=" + start + "&end=" + end, function(events) {
    var eventMap = parseEvents(events);
    var max = eventMap["max"];
    for (var key in eventMap) {
      if (key == "max") continue;
      var hours = $("<div>");
      for (var hour = 0; hour < 24; hour++) {
        var color = 256 - Math.min(256, Math.floor(256 * eventMap[key][hour].length / max));
        hours.append($("<div>")
          .addClass("hour")
          .css("background-color", "rgb(" + color + "," + color + "," + color + ")")
          .css("border-color", eventMap[key][hour].length ? "rgb(150,150,150)" : "rgb(235,235,235)")
          .attr("key", key)
          .attr("day", $("#cell" + key).attr("day"))
          .attr("hour", hour)
          .click(function () {
            var key = $(this).attr("key");
            var hour = $(this).attr("hour");
            showDetails(parseInt(key[0]), parseInt(key[1]), parseInt(hour), eventMap[key], $(this));
          })
        );
      }
      $("#cell" + key)
        .find(".number")
        .append(hours);
    }
  })
}

function showDetails(weekIndex, dayIndex, hour, day, dayDiv) {
  var eventCountByUser = {};
  for (var n = 0; n < day[hour].length; n++) {
    var event = day[hour][n];
    var key = event[INDEX_USER];
    if (key) {
      if (key.indexOf("@") == -1) {
        key = event[INDEX_APP_NAME];
      } else {
        var domain = event[INDEX_URL].replace(/https?:\/\//, "").replace(/\/.*/, "");
        key += " - " + domain;
      }
      eventCountByUser[key] = (eventCountByUser[key] || 0) + 1;
    }
  }
  createPieChart(eventCountByUser, dayIndex, dayDiv.attr("day"), hour);
}

function createPieChart(eventCountByUser, dayIndex, day, hour) {
  var dataPoints = [];
  for (key in eventCountByUser) {
    dataPoints.push({ label: key, value: eventCountByUser[key] });
  }
  $("#details").empty();
  new d3pie("details", {
    header: {
      title: {
        text: "Details for " + MONTH_NAMES[currentDate.getMonth()] + " " + day + " - " + hour + ":00 - " + (hour+1) + ":00",
        fontSize: 30,
        margin: 24,
      },
      subtitle: {
        text: " ",
        color: "#999999",
        fontSize: 12,
        font: "open sans"
      },
      titleSubtitlePadding: 59
    },
    size: {
      canvasWidth: 1200,
      pieOuterRadius: "90%"
    },
    labels: {
      outer: {
        pieDistance: 32
      },
      inner: {
        hideWhenLessThanPercentage: 3
      },
      mainLabel: {
        fontSize: 17
      },
    },
    data: {
      content: dataPoints
    }
  });
  $("#details").dialog({
    width: 1200,
    height: 900,
    modal: true,
  });
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
        .attr("day", day)
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

$("td.day").click(function() {
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

setInterval(render, 1000 * 60);

render();
