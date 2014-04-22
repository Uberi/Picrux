//wip: move the time and settings stuff to the right side in its own pane for each entry
//wip: store data in a database to support larger datasets
//wip: import from google tasks and whatever
//wip: entry_drafting for in-place editing of entries

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
	$(".entry_drafting").hide();

	// button handlers
	$(".trash").click(function(event) {
		var element = $(event.delegateTarget).parents(".entry, .entry_drafting");
		if (element.hasClass("entry_drafting")) { // clear and reset the editing entry //wip: maybe handle this in Entry.remove
			editor.setValue(""); //wip: show an undo banner
			element.hide();
		} else
			Entry.remove(element.get(0));
		if ($("#items .entry").length === 0) $("#empty_message").show();
	});

	// editing handlers
	$("#time_entry").change(function(event) {
		var element = $(event.target).parents(".entry_drafting");
		var time = $(event.target).val();
		Entry.time(element, time === "" ? null : time);
	});
	$(".add").click(function(event) {
		var element = $(event.target).parents(".entry_drafting");
		var time = Entry.time(element);
		var message = editor.getDoc().getValue();
		Entry.create(time, message);
		editor.setValue("");
		element.hide();
		$("#empty_message").hide();
	});

	if ($("#items .entry").length === 0) $("#empty_message").show();
	else $("#empty_message").hide();
}

var updateEditingEntry = function(entry, userMessage) {
	// reset marked ranges
	var doc = editor.getDoc();
	var marks = doc.getAllMarks();
	for (var i = 0; i < marks.length; i ++) marks[i].clear();

	// parse and update times embedded in the message
	var times = chrono.parse(userMessage);
	var time_list = $("#time_entry").empty();
	for (var i = 0; i < times.length; i ++) {
		var startDate = moment(times[i].startDate);
		var endDate = moment(times[i].endDate);
		var humanDate = startDate.fromNow(); //wip: handle ranges

		// add an option to select the time
		time_list.append("<option value=\"" + startDate.unix() + "\">" + humanDate + "</option>");

		// mark the location in the text where the time was found
		var startPosition = doc.posFromIndex(times[i].index);
		var endPosition = doc.posFromIndex(times[i].index + times[i].text.length);
		doc.markText(startPosition, endPosition, {className: "time_text", title: humanDate});
	}
	time_list.append("<option value=\"\">N/A</option>");
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
	return function(doc, change) {
		clearTimeout(currentTimer);
		currentTimer = setTimeout(function () {
			var value = doc.getValue();
			var entry = $(".entry_drafting");
			updateEditingEntry(entry, value);
		}, 300);
	};
}()