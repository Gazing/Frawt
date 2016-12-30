$.ajax({
	url: "/api/time",
	success: function(result) {
		ampm = "PM"
		if (result <= "12:00") {
			ampm = "AM"
		}
		$("body").append("<h2><p>Current Server Time: "+result+" "+ampm+"</p></h2>");
	}
});

$.ajax({
	url: "/api/rooms/available",
	headers: {"start": "12:00", "end":"15:00"},
	success: function(result) {
		$("body").append("<p>");
		for (i = 0; i < result.length; i++) {
			if (i % 6 == 0) {
				$("body").append("</p>\n<p>");
			}
			$("body").append(result[i]["room_name"]+" | ");
		}
	}
});
