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
	
	var start = parseInt($("#start-time").val().split(" ")[0].split(":")[0]);
	if ($("#start-time").val().indexOf("AM") == -1) {
		start += 12;
	}
	var end = parseInt($("#end-time").val().split(" ")[0].split(":")[0]);
	if ($("#end-time").val().indexOf("AM") == -1) {
		end += 12;
	}
	$.ajax({
		url: "/api/rooms/available",
		headers: {"start": start+":00", "end": end+":00"},
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
    timeFormat: 'h:mm p',
    interval: 60,
    minTime: '0',
    maxTime: '11:00pm',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
	change: on_time_change
	});
});

$(document).ready(function(){
    $('#end-time').timepicker({
    timeFormat: 'h:mm p',
    interval: 60,
    minTime: '0',
    maxTime: '11:00pm',
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
			var ampm = "PM";
			if (result <= "12:00") {
				ampm = "AM";
			} else {
				start = parseInt(result.split(":")[0])-12;
				start = start+":00";
			}
			
			$("#start-time").val(start+" "+ampm);
			ampm = "AM";
			var end = parseInt(result.split(":")[0])+1;
			if (end > 12) {
				end -= 12;
				ampm = "PM";
			}
			$("#end-time").val(end+":00 "+ampm);
			clearTable();
			on_time_change();
		}
	})
});