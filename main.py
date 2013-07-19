#wip: search by description, time range

# import standard libraries
from os import path
import json

# import utility libraries
import recurrent
from dateutil import parser
from dateutil import rrule
from datetime import datetime
import ago

# import application libraries
import controls as tk

class Entry:
    def __init__(self, description, target=None):
        r = recurrent.RecurringEvent()
        self.description = description
        if target:
            self.recurring = "RRULE" in target
            if self.recurring:
                self.target = target
            else:
                self.target = parser.parse(target)
        else:
            self.target = r.parse(description)
            self.recurring = r.is_recurring
        if self.recurring:
            self.rule = rrule.rrulestr(self.target, cache=True)

    def occurrence(self):
        """Returns a datetime representing the next occurrence of the event."""
        if self.recurring:
            return self.rule.after(datetime.now()) # obtain next occurrence of recurring rule
        return self.target

    def occurrence_readable(self):
        """Returns the next occurrence of the event as a human-readable string."""
        return ago.human(self.occurrence(), 3)

def bind_tag(tag, *widgets):
    """Bind a given tag as the first bindtag for each given widget"""
    for widget in widgets:
        widget.bindtags((tag,) + widget.bindtags())

def entry_active(event): # called upon hovering or focusing on an entry
    event.widget.config(style="Active.Entry.TFrame") # set frame as active
    children = event.widget.winfo_children()
    label = [x for x in children if x.winfo_class() == "TLabel"][0] # find label in the frame
    label.config(style="Active.Entry.TLabel") # set label as active

def entry_inactive(event): # called upon stopping of hovering or focusing on an entry
    event.widget.config(style="Entry.TFrame") # set frame as active
    children = event.widget.winfo_children()
    label = [x for x in children if x.winfo_class() == "TLabel"][0] # find label in the frame
    label.config(style="Entry.TLabel") # set label as active

def update(master, entries):
    for index, entry in enumerate(entries):
        text = entry.occurrence_readable()
        frame = get_entry(master, index)
        frame.winfo_children()[2]["text"] = text
    w.after(1000, lambda: update(master, entries))
    return

def load():
    try:
        # load the settings from the settings file
        with open(settings, "r") as f:
            result = json.load(f)
        entries = []
        for value in result["entries"]:
            entries.append(Entry(value["description"], value["target"]))
        search.previous = result["search"]
        return entries
    except IOError:
        return []

def save(entries, search):
    values = [{"description": e.description, "target": str(e.target)} for e in entries]
    result = {"entries": values, "search": search}
    with open(settings, "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4, separators=(",", ": "))

current_search = ""

def search():
    global current_search
    search_handler.timer = None
    value = search_box.get()
    if value == current_search:
        return
    current_search = value
    if value == "":
        indicator.config(text="+")
    else:
        indicator.config(text="\u25b6")
    list = [entry.description for entry in entries if value in entry.description]
    print(list)

def search_handler(event):
    self = search_handler
    if self.timer != None: # current timer is active
        search_box.after_cancel(self.timer) # cancel current timer
    self.timer = search_box.after(300, search) # start new timer
search_handler.timer = None

def add_reminder(index, description):
    entry = Entry(description)
    entries.append(entry)
    add_entry(scroll_area.interior, index, entry)

def get_entry(master, index):
    return master.grid_slaves(index, 0)[0]

def add_entry(master, index, entry): # add a new entry to the bottom of the entries list
    frame = tk.Frame(master, padding=10, style="Entry.TFrame")
    frame.grid(row=index, column=0, sticky=tk.NSEW, padx=1, pady=1)
    frame.bind("<Enter>", entry_active)
    frame.bind("<Leave>", entry_inactive)
    frame.bind("<FocusIn>", entry_active)
    frame.bind("<FocusOut>", entry_inactive)
    label = tk.Label(frame, text=entry.description, style="Entry.TLabel")
    label.pack(anchor=tk.NW, padx=5, pady=5)
    bind_tag("entry", frame, label) # bind a tag to each element in the entry
    frame.bind_class("entry", "<Return>", expand_entry)
    frame.bind_class("entry", "<Button>", expand_entry)
    tk.Button(frame, text="\u2715", width=2).pack(side=tk.RIGHT)
    tk.Label(frame, relief=tk.SOLID, padding=5).pack(side=tk.LEFT, padx=5, pady=5)

def expand_entry(event):
    widget = event.widget
    if widget.winfo_class() != "TFrame": # child entry selected
        widget = widget.nametowidget(widget.winfo_parent()) # ensure frame is selected
    print(get_entry(scroll_area.interior, 0).winfo_children()[0]["text"])

settings = path.join(path.dirname(path.realpath(__file__)), "settings.conf")
font = "Arial" #wip: check if font is available

entries = load()

# create window
w = tk.Tk()
w.title("Picrux")
w.config(background="white")
w.protocol("WM_DELETE_WINDOW", w.destroy)
w.rowconfigure(0, weight=1)
w.columnconfigure(0, weight=1)

# create scrollable container
scroll_area = tk.VerticalScrolledFrame(w, borderwidth=1, relief=tk.SOLID)
scroll_area.interior.config(padding=1)
scroll_area.interior.columnconfigure(0, weight=1)
scroll_area.grid(row=0, sticky=tk.NSEW, padx=10, pady=10)

# add test entries
for index, entry in enumerate(entries):
    add_entry(scroll_area.interior, index, entry)

area = tk.Frame(w, style="Container.TFrame")
area.grid(row=1, sticky=tk.NSEW, padx=10, pady=(0, 10))
area.columnconfigure(0, weight=1)

# create search box
search_box = tk.Entry(area, font=(font, 18), style="Search.TEntry")
search_box.insert(0, search.previous)
search_box.grid(row=0, column=0, sticky=tk.NSEW)
search_box.bind("<Key>", search_handler)

indicator = tk.Button(area, text="+", style="Action.TButton", width=2)
indicator.grid(row=0, column=1, sticky=tk.NSEW, padx=(5, 0))
indicator.columnconfigure(1, weight=1)

# apply styling to widgets
s = tk.Style()
s.theme_use("clam")
s.configure("Container.TFrame", background="white")
s.configure("Entry.TFrame", background="white", padding=20, relief=tk.GROOVE)
s.configure("Entry.TLabel", font=(font, 18), background="white")
s.configure("Active.Entry.TFrame", background="#efe5e5")
s.configure("Active.Entry.TLabel", font=(font, 18), background="#efe5e5")
s.configure("TButton", font=(font, 12), background="#c05050", padding=2)
s.map("TButton", background=[("pressed", "#f50202"), ("active", "#f50202"), ("focus", "#f50202")])
s.configure("TLabel", font=(font, 8), background="white")
s.configure("Search.TEntry", padding=5)
s.configure("Action.TButton", font=(font, 32), background="white", padding=0)

# set minimum size of the window to current size
w.update()
w.minsize(w.winfo_width(), w.winfo_height())

search_box.focus()

update(scroll_area.interior, entries)

w.mainloop()

save(entries, search.previous)