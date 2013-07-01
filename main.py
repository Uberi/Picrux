# import standard libraries
from os import path
import json
from tkinter import *
from tkinter.ttk import *

# import utility libraries
import recurrent
from dateutil import rrule
from datetime import datetime

# import application libraries
from controls import *

def load():
    try:
        with open(settings, "r") as f:
            entries = json.load(f)
        return entries
    except IOError:
        pass
    return []

def save(entries):
    with open(settings, "w+") as f:
        json.dump(entries, f)

def search():
    self = search
    search_handler.timer = None
    value = search_box.get()
    if value == self.previous:
        return
    self.previous = value
    if value == "":
        indicator.config(text="\u25c6")
    else:
        indicator.config(text="\u25b6")
search.previous = ""

def search_handler(event):
    self = search_handler
    if self.timer != None: # current timer is active
        search_box.after_cancel(self.timer) # cancel current timer
    self.timer = search_box.after(300, search) # start new timer
search_handler.timer = None

def add_entry(master, description, remaining): # add a new entry to the bottom of the entries list
    frame = Frame(master, padding=10, style="Entry.TFrame")
    frame.pack(anchor=NW, fill=X, expand=True, padx=1, pady=1)
    frame.bind("<Enter>", entry_active)
    frame.bind("<Leave>", entry_inactive)
    frame.bind("<FocusIn>", entry_active)
    frame.bind("<FocusOut>", entry_inactive)
    label = Label(frame, text=description, style="Entry.TLabel")
    label.pack(anchor=NW, padx=5, pady=5)
    bind_tag("entry", frame, label) # bind a tag to each element in the entry
    frame.bind_class("entry", "<Return>", expand_entry)
    frame.bind_class("entry", "<Button>", expand_entry)
    Button(frame, text=remaining).pack(anchor=SE, padx=5, pady=5)

def expand_entry(event):
    print("test")

settings = path.join(path.dirname(path.realpath(__file__)), "settings.conf")
font = "Segoe UI" #wip: check if font is available

entries = load()

# create window
w = Tk()
w.title("Picrux")
w.config(background="white")
w.protocol("WM_DELETE_WINDOW", w.destroy)

# create scrollable container
scroll_area = VerticalScrolledFrame(w, borderwidth=1, relief=SOLID)
scroll_area.interior.config(padding=1)
scroll_area.pack(anchor=NW, fill=BOTH, expand=1, padx=10, pady=10)

# add test entries
for i in range(20):
    add_entry(scroll_area.interior, "do something %s" % i, "ITEM TIME REMAINING %s" % i)

# create search box
search_box = Entry(w, font=(font, 18), style="Search.TEntry")
search_box.pack(side=LEFT, fill=X, expand=True, padx=(10, 5), pady=10)
search_box.bind("<Key>", search_handler)

#indicator = Label(w, text="+", style="Action.TLabel")
#indicator = Label(w, text="\u25b6", style="Action.TLabel")
indicator = Label(w, text="\u25c6", style="Action.TLabel")
indicator.pack(side=RIGHT, padx=(0, 10), pady=(0, 10))

# apply styling to widgets
s = Style()
s.theme_use("clam")
s.configure("Entry.TFrame", background="white", padding=20, relief=GROOVE)
s.configure("Entry.TLabel", font=(font, 18), background="white")
s.configure("Active.Entry.TFrame", background="#efe5e5")
s.configure("Active.Entry.TLabel", font=(font, 18), background="#efe5e5")
s.configure("TButton", font=(font, 8), background="white")
s.configure("Search.TEntry", padding=5)
s.configure("Action.TLabel", font=(font, 32), background="white", padding=0)

# set minimum size of the window to current size
w.update()
w.minsize(w.winfo_width(), w.winfo_height())

search_box.focus()

w.mainloop()

save(entries)

r = recurrent.RecurringEvent()
value = r.parse("do the laundry every friday at 6")
if r.is_recurring:
    value = rrule.rrulestr(value).after(datetime.now()) # obtain next occurence of recurring rule
print(value)