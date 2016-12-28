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
	console.log("Changed");
}

$(document).ready(function(){
    $('#start-time').timepicker({
    timeFormat: 'h:mm p',
    interval: 60,
    minTime: '0',
    maxTime: '11:00pm',
    defaultTime: '11',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
	change: on_time_change
	});
});

$(document).ready(function(){
    for (var i = 0; i < 70; i++) {
		$("#result_body").append("<tr><td>Lorem Ipsum "+i+"</td></tr>");
	}
});

$(document).ready(function(){
    $('#end-time').timepicker({
    timeFormat: 'h:mm p',
    interval: 60,
    minTime: '0',
    maxTime: '11:00pm',
    defaultTime: '11',
    startTime: '00:00',
    dynamic: false,
    dropdown: true,
    scrollbar: true,
	change: on_time_change
	});
});