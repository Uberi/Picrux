// all functions accept jQuery objects as elements and unix time offsets as times

// mock server side for browser testing
if (typeof _server_side_ === "undefined") {
	_server_side_ = {
		create: function() {
			var counter = 0;
			return function(time, message) { return counter ++; };
		}(),
		remove: function(id) {},
		time: function(id, time, remove) {},
		message: function(id, message) {},
	};
}

var Entry = {
	// creates an entry and returns its new DOM element
	create: function(time, message) {
		var id = _server_side_.create(time, message);
		var entry = $("#items").append(
			"<li class=\"entry\">" +
				"<div class=\"time\" data-time=\"" + time + "\" data-id=\"" + id + "\"></div>" +
				"<div class=\"message\">" + message + "</div>" +
			"</li>");
		Entry.updateTime(entry);
		return entry;
	},
	// removes a given entry
	remove: function(element) {
		_server_side_.remove(element.data("id"));
		element.remove();
	},
	// deletes, retrieves, or sets the time of a given entry, returning the UNIX timestamp if retrieving
	time: function(element, newTime) {
		var value = element.find(".time");
		if (newTime === null) { // time is to be deleted
			_server_side_.time(value.data("id"), 0, false);
			value.removeData("time");
		}
		else if (!newTime) { // new time not specified, simply produce the timestamp
			var timestamp = value.data("time");
			if (typeof timestamp === "undefined")
				return null;
			return timestamp;
		}
		else { //time is to be updated
			_server_side_.time(value.data("id"), newTime, true);
			value.data("time", newTime);
		}
		Entry.updateTime(element);
	},
	// updates or retrieves a given entry's Markdown contents, returning the markdown if retrieving
	message: function(element, message) {
		var value = element.find(".message");

		if (!message) // retrieve message
			return value.html();

		// convert MarkDown to HTML
		var valueHTML = marked(message, {
			gfm: true, tables: true, breaks: true, sanitize: false, //wip: set it to sanitize if running on the web
			smartLists: true, smartypants: true,
		});
		_server_side_.message(message);
		value.html(valueHTML);
	},
	// updates the time display of a given entry
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