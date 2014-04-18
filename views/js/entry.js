// all functions accept jQuery objects as elements and unix time offsets as times

//wip: sync entries with server
var Entry = {
	create: function(time, message) {
        var entry = $("#items").append(
			"<li class=\"entry\">" +
				"<div class=\"time\" data-time=\"" + time + "\"></div>" +
				"<div class=\"message\">" + message + "</div>" +
			"</li>");
        Entry.updateTime(entry);
		return entry;
	},
	remove: function(element) {
		element.remove();
	},
	time: function(element, newTime) {
		var value = element.find(".time");
		if (newTime === null) {
			value.removeData("time");
		}
		else if (!newTime) {
			var timestamp = value.data("time");
			
			if (typeof timestamp === "undefined")
				return null;
			return timestamp;
		}
		else
			value.data("time", newTime);
		Entry.updateTime(element);
	},
	message: function(element, newMessage) {
		var value = element.find(".message");
		if (!newMessage)
			return value.html();
		value.html(newMessage);
	},
	updateTime: function(element) {
		var timestamp = Entry.time(element);
		if (timestamp === null) {
			element.find(".time").text("(no deadline)");
			element.removeClass("past");
		}
		else {
			var time = moment.unix(timestamp);
			element.find(".time").text(time.fromNow());
			if (time.isBefore())
				element.addClass("past");
			else
				element.removeClass("past");
		}
	}
}