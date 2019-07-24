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
var lastEvents = [];

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
    var timestamp = event[INDEX_TIMESTAMP];
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
    lastEvents = events;
    var eventMap = parseEvents(events);
    for (var key in eventMap) {
      if (key == "max") continue;
      var hours = $("<div>").addClass("day-hours");
      var totalCoverage = 0;
      for (var hour = 0; hour < 24; hour++) {
        var coverage = getSampleCoverage(eventMap[key][hour]);
        totalCoverage += coverage;
        var color = 256 - Math.floor(coverage * 256);
        var minutes = Math.floor(coverage * 60);
        hours.append($("<div>")
          .addClass("hour")
          .css("background-color", "rgb(" + color + "," + color + "," + color + ")")
          .css("border-color", eventMap[key][hour].length ? "rgb(150,150,150)" : "rgb(235,235,235)")
          .attr("key", key)
          .attr("day", $("#cell" + key).attr("day"))
          .attr("hour", hour)
          .attr("minutes", minutes)
          .click(function () {
            var key = $(this).attr("key");
            var hour = $(this).attr("hour");
            var minutes = $(this).attr("minutes");
            showDetails(eventMap[key], key, parseInt(hour), minutes, $(this));
          })
        );
      }
      $("#cell" + key)
        .find(".number")
        .append([
          $("<div>")
            .addClass("detail-day-hours")
            .text(totalCoverage.toFixed(1) + " hours"),
          hours
        ]);
    }
  })
}

function getSampleCoverage(events) {
  var samples = {}
  for (var n = 0; n < events.length; n++) {
    var event = events[n];
    var timestamp = event[INDEX_TIMESTAMP];
    for (var k = -5; k < 5; k++) {
      samples[timestamp + k] = event;
    }
  }
  return Object.keys(samples).length / 3600;
}

function showMatching(label) {
  // TODO
}

function showDetails(dayEvents, key, hour, minutes, dayDiv) {
  var eventCountByUser = {};
  for (var n = 0; n < dayEvents[hour].length; n++) {
    var event = dayEvents[hour][n];
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
  createPieChart(eventCountByUser, dayDiv.attr("day"), hour, minutes);
  createDayChart(dayEvents);
  showDetailsDialog();
}

function showDetailsDialog() {
  $("#details").dialog({
    width: 1200,
    height: 900,
    modal: true,
  });
}

function createDayChart(dayEvents) {
  // TODO
  for (var hour = 0; hour < 25; hour++) {
    $("#details-day").append($("<div>")
      .addClass("detail-hour-marker")
      .html(hour < 24 ? hour : "&nbsp;"));
  }
}

function createPieChart(eventCountByUser, day, hour, minutes) {
  var dataPoints = [];
  for (key in eventCountByUser) {
    var value = eventCountByUser[key];
    if (value > 2) {
      dataPoints.push({ label: key, value: value });
    }
  }
  $("#details-pie").empty();
  $("#details-day").empty();
  new d3pie("details-pie", {
    header: {
      title: {
        text: "Details for " + minutes + " minutes during " + MONTH_NAMES[currentDate.getMonth()] + " " + day + " - " + hour + ":00 - " + (hour+1) + ":00",
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
      content: dataPoints,
      sortOrder: "value-asc",
    },
    callbacks: {
      onClickSegment: function(segment) {
        showMatching(segment.data.label);
      }
    }
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
