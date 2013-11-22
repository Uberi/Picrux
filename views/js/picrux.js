var main = function() {
	var editor = CodeMirror.fromTextArea($("#search_add > textarea").get(0), {
		placeholder: "search or add entries...",
		mode: "gfm",
		theme: "blackboard",
		autofocus: true,
		lineWrapping: true,
	});
	updateTimes();
	setInterval(updateTimes, 1000);
	
	// fade in the entries
	$(".entry").hide().fadeIn();
}

var Entry = {
	create: function(time, message) {
		var element = $("#items") //wip: add an entry;
		//wip: figure out how to make this work with "new"
		return {
			time: time,
			message: message,
			element: element,
			__proto__: Entry,
		};
	},
	destroy: function() {
		//wip: remove the element
	},
};

var updateTimes = function() {
	$(".time").each(function(i, e) {
		var element = $(e);
		var time = moment.unix(element.data("time"));
		element.text(time.fromNow());
		if (time.isBefore())
			element.parent().addClass("past");
	})
}

var onAddSearchChange = function() {
	var currentTimer;
	return function(cm, change) {
		clearTimeout(currentTimer);
		currentTimer = setTimeout(function() {
			cm.getValue();
			//wip: render the HTML and update the element
		}, 1000);
	};
}()