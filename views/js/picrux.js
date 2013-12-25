//wip: move the time and settings stuff to the right side in its own pane for each entry

var SERVER_ADDRESS = "http://localhost:222/";

var main = function() {
	// editor setup
	var editor = CodeMirror.fromTextArea($("#search_add > textarea").get(0), {
		placeholder: "search or add entries...",
		mode: "gfm",
		theme: "blackboard",
		autofocus: true,
		lineWrapping: true,
	});
	editor.on("change", onAddSearchChange);
	
	// update times every second
	setInterval(function() {
		$(".entry").each(function(index, entry) {
			Entry.updateTime($(entry));
		})
	}, 1000);
	
	// fade in the entries
	$(".entry").hide().fadeIn();
}

var updateTemporaryEntry = function(userMessage) {
	var entry = $(".entry_editing");
	
	// parse times embedded in the message
	$.get(SERVER_ADDRESS + "parse_time", userMessage, function(time) {
		if (time === "")
			Entry.time(entry, null);
		else // time value found
			Entry.time(entry, parseInt(time));
	}, "text");
	
	// convert the markdown to HTML
	var valueHTML = marked(userMessage, {
		gfm: true, tables: true, breaks: true, sanitize: false,
		smartLists: true, smartypants: true,
	});
	entry.find(".message").html(valueHTML);
}

// calls `updateTemporaryEntry` when the editor has not changed for a while
var onAddSearchChange = function() {
	var currentTimer;
	return function(cm, change) {
		clearTimeout(currentTimer);
		currentTimer = setTimeout(function () {
			var value = cm.getValue();
			updateTemporaryEntry(value);
		}, 500);
	};
}()

// all functions accept jQuery objects as elements and unix time offsets as times
var Entry = {
	create: function(time, message) {
		return $("#items").append(
			"<li class=\"entry\">" +
				"<div class=\"time\" data-time=\"" + time + "\"></div>" +
				"<div class=\"message\">" + message + "</div>" +
			"</li>");
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
			element.find(".time").text("");
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