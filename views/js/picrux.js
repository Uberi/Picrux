//wip: move the time and settings stuff to the right side in its own pane for each entry
//wip: store data in a database to support larger datasets
//wip: import from google tasks and whatever

var editor = null;

var main = function() {
	// editor setup
	editor = CodeMirror.fromTextArea($("#search_add > textarea").get(0), {
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

	// set up syntax highlighting in the entries
	marked.setOptions({
		highlight: function (code, lang) {
			if (typeof lang === "string")
				return hljs.highlight(lang, code).value;
			return hljs.highlightAuto(code).value;
		}
	});

	// don't show the entry preview initially
	$(".entry_editing").hide();

	// button handlers
	$(".trash").click(function(event) {
		var element = $(event.delegateTarget).parents(".entry, .entry_editing");
		Entry.remove(element.get(0));
	});
}

var updateEditingEntry = function(entry, userMessage) {
	// parse and update times embedded in the message
	var times = chrono.parse(userMessage);
	var time_list = $("#time_entry").empty();
	var doc = editor.getDoc();
	for (var i = 0; i < times.length; i ++) {
		var startDate = moment(times[i].startDate);
		var endDate = moment(times[i].endDate);
		var humanDate = startDate.fromNow(); //wip: handle ranges

		// add an option to select the time
		time_list.append("<option value=\"" + times[i].text + "\">" + humanDate + "</option>");

		// mark the location in the text where the time was found
		var startPosition = doc.posFromIndex(times[i].index);
		var endPosition = doc.posFromIndex(times[i].index + times[i].text.length);
		doc.markText(startPosition, endPosition, {className: "time_text", title: humanDate});
	}
	time_list.append("<option value=\"N/A\">N/A</option>");
	if (times.length > 0) Entry.time(entry, moment(times[0].startDate).unix()); //wip: support time ranges
	else Entry.time(entry, null);

	// show entry only if there is a message
	if (userMessage === "") entry.hide();
	else {
		Entry.message(entry, userMessage);
		entry.show();
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