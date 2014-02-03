//wip: move the time and settings stuff to the right side in its own pane for each entry
//wip: store data in a database to support larger datasets
//wip: import from google tasks and whatever

var main = function() {
	// editor setup
	var editor = CodeMirror.fromTextArea($("#search_add > textarea").get(0), {
		mode: "gfm",
		theme: "paraiso-light",
		autofocus: true,
		lineWrapping: true,
	});
	editor.on("change", onAddSearchChange); // update the preview whenever needed
    
    // set up fixed header positioning
    var search = $("#search_add");
    var content = $("#content");
    search.css({"position": "fixed", "top": 0, "width": "100%", "z-index": 2});
    editor.on("change", function(cm, change) {
        content.css("margin-top", search.outerHeight() + "px");
    });
    content.css("margin-top", search.outerHeight() + "px");
	
	// update entry times every second
    var updateAll = function() {
		$(".entry").each(function(index, entry) {
			Entry.updateTime($(entry));
		})
	};
    updateAll();
	setInterval(updateAll, 1000);
	
	// set up syntax highlighting
	marked.setOptions({
		highlight: function (code, lang) {
			if (typeof lang === "string")
				return hljs.highlight(lang, code).value;
			return hljs.highlightAuto(code).value;
		}
	});
	
	// don't show the entry preview initially
	$(".entry_editing").hide();
}

var updateEditingEntry = function(entry, userMessage) {
	// parse times embedded in the message
    if (window._python_side_) { // Python side API available
        var time = _python_side_.parse_time(userMessage)
        if (time === "")
            Entry.time(entry, null);
        else // time value found
            Entry.time(entry, parseInt(time));
    }
	
	// convert the markdown to HTML
	var valueHTML = marked(userMessage, {
		gfm: true, tables: true, breaks: true, sanitize: false,
		smartLists: true, smartypants: true,
	});

	if (valueHTML === "") // entry preview is blank
		entry.hide();
	else {
		entry.show();
        Entry.message(entry, valueHTML);
    }
}

// calls `updateTemporaryEntry` when the editor has not changed for a while
var onAddSearchChange = function() {
	var currentTimer;
	return function(cm, change) {
		clearTimeout(currentTimer);
		currentTimer = setTimeout(function () {
			var value = cm.getValue();
			var entry = $(".entry_editing");
			updateEditingEntry(entry, value);
		}, 300);
	};
}()

// all functions accept jQuery objects as elements and unix time offsets as times
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