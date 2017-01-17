// JavaScript Document

function search_click() {
	"use strict";
	var form = document.getElementById("filter_form");
	
	// var res = document.getElementById("result_form");
	var isOpen = form.classList.contains('slide-in');
    form.setAttribute('class', isOpen ? 'slide-out form_box' : 'slide-in form_box');
}

function on_time_change() {
	"use strict";
	var start = $("#start-time").val();
	var end = $("#end-time").val();
	var day = $("#day-time").val();
	$.ajax({
		url: "/api/rooms/available",
		headers: {"start": start, "end": end, "day": day},
		success: function(result) {
			clearTable();
			for (var i = 0; i < result.length; i++) {
				$("#result_body").append("<tr><td>"+result[i]["room_name"]+"</td></tr>");
			}
		},
		error: function(xhr, textStatus, errorThrown) {
			clearTable();
			$("#result_body").append("<tr><td>Failed to retrieve data. Make sure From and To are correct.</td></tr>");
		}
	});
}

function clearTable() {
	"use strict";
	$("#result_body tr").remove();
}

$(document).ready(function(){
	"use strict";
    $('#start-time').timepicker({
    	'step': 60,
		'show2400': true,
		'timeFormat': 'H:i',
		'disableTextInput': true
	});
	$('#start-time').on("changeTime", on_time_change);
});

$(document).ready(function(){
	"use strict";
    $('#end-time').timepicker({
    	'step': 60,
		'show2400': true,
		'timeFormat': 'H:i',
		'disableTextInput': true
	});
	$('#end-time').on("changeTime", on_time_change);
});

$(document).ready(function(){
	"use strict";
    $.ajax({
		url: "/api/time",
		success: function(result) {
			
			var start = result["time"].split(":")[0];
			var end = parseInt(start)+1;
			if (end == 24) {
				end = "00";
			}
			$("#start-time").val(start+":00");
			$("#end-time").val(end+":00");
			$("#day-time").val(result["day"]);
			clearTable();
			on_time_change();
		}
	});
});

$(document).ready(function() {
	"use strict";
	$('#day-time').timepicker({
		'noneOption': [{'label': "Monday", 'value': 'Monday'},
					   {'label': "Tuesday", 'value': "Tuesday"}, 
					   {'label': "Wednesday", 'value': "Wednesday"}, 
					   {'label': "Thursday", 'value': "Thursday"},
					   {'label': "Friday", 'value': "Friday"}],
		'minTime': "",
		'maxTime': "",
		'disableTextInput': true,
	});
	$('#day-time').on("changeTime", on_time_change);
});

$(document).ready(function() {
	document.getElementById("day-time").addEventListener("click", function() {
		$(".ui-timepicker-am").remove();
		document.getElementById("day-time").removeEventListener("click");
	});
});
