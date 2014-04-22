// all functions accept jQuery objects as elements and unix time offsets as times

// mock server side for browser testing
if (typeof _server_side_ === "undefined") {
	_server_side_ = {
		create: function() {
			var counter = 0;
			return function(time, message, has_time) { return counter ++; };
		}(),
		remove: function(entry_index) {},
		time: function(entry_index, time, remove) {},
		message: function(entry_index, message) {},
	};
}

var Entry = {
	// creates an entry and returns its new DOM element
	create: function(time, message) {
		var id;
		if (time === null) id = _server_side_.create(0, message, false);
		else id = _server_side_.create(time, message, true);
		var entry = $("#items").append(
			"<li class=\"entry\" data-id=\"" + id + "\">" +
				"<div class=\"actions\">" +
					"<div class=\"time\" data-time=\"" + time + "\"></div>" +
					"<div>" +
						"<a href=\"#\" class=\"trash\"><div class=\"lid\"></div><div class=\"can\"></div></a>" +
						"<a href=\"#\" class=\"edit\"><div class=\"pencil\"></div></a>" +
					"</div>" +
				"</div>" +
				"<div class=\"message\">" + message + "</div>" +
				"<div class=\"overlay\"></div>" +
			"</li>"
		);
		Entry.updateTime(entry);
		return entry;
	},
	// removes a given entry
	remove: function(element) {
		var entry = $(element);
		_server_side_.remove(entry.data("id"));
		entry.css("min-height", 0);
		entry.animate({opacity: 0, height: 0}, 100, function() { //wip: show an undo banner
			entry.remove();
		});
	},
	// deletes, retrieves, or sets the time of a given entry, returning the UNIX timestamp if retrieving
	time: function(element, newTime) {
		var value = element.find(".time");
		if (newTime === null) { // time is to be deleted
			_server_side_.time(element.data("id"), 0, false);
			value.removeData("time");
		}
		else if (!newTime) { // new time not specified, simply produce the timestamp
			var timestamp = value.data("time");
			if (typeof timestamp === "undefined")
				return null;
			return timestamp;
		}
		else { //time is to be updated
			_server_side_.time(element.data("id"), newTime, true);
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
		_server_side_.message(element.data("id"), message);
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