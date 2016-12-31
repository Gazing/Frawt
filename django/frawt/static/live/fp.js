// JavaScript Document

function search_click() {
	var form = document.getElementById("filter_form");
	var res = document.getElementById("result_form");
	var isOpen = form.classList.contains('slide-in');
    form.setAttribute('class', isOpen ? 'slide-out form_box' : 'slide-in form_box');
	var outmargin = -107+form.clientHeight;
	res.style.marginTop = isOpen ? '-107px' : outmargin+'px';
	
}

function on_time_change() {
	
	var start = $("#start-time").val();
	var end = $("#end-time").val();
	$.ajax({
		url: "/api/rooms/available",
		headers: {"start": start, "end": end},
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
	$("#result_body tr").remove();
}

$(document).ready(function(){
    $('#start-time').timepicker({
    timeFormat: 'HH:mm',
    interval: 60,
    minTime: '0',
    maxTime: '23:00',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
	change: on_time_change
	});
});

$(document).ready(function(){
    $('#end-time').timepicker({
    timeFormat: 'HH:mm',
    interval: 60,
    minTime: '0',
    maxTime: '23:00',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
	change: on_time_change
	});
});

$(document).ready(function(){
    $.ajax({
		url: "/api/time",
		success: function(result) {
			var start = result.split(":")[0];
			var end = parseInt(start)+1;
			$("#start-time").val(start+":00");
			$("#end-time").val(end+":00");
			clearTable();
			on_time_change();
		}
	})
});