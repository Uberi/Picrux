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
	// parse and update times embedded in the message
    var times = chrono.parse(userMessage);
    var time_list = $("#time_list").empty();
    for (var i = 0; i < times.length; i ++) {
        var start = moment(times[i].startDate);
        var end = moment(times[i].endDate);
        time_list.append("<option value=\"" + times[i].text + "\">" + start.fromNow() + "</option>");
        //wip: userline the date text like in gmail
    }
    if (times.length > 0) {
        $("#time_entry").val(times[0].text);
        Entry.time(entry, moment(times[0].startDate).unix()); //wip: support time ranges
    }
    else {
        $("#time_entry").val(times[0].text);
        Entry.time(entry, null);
    }
    Entry.message(entry, userMessage);
    
    // show entry only if there is a message
	if (Entry.message(entry) === "") entry.hide();
	else entry.show();
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