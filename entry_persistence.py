import os, json
from PySide import QtCore

SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reminders.json")
TIMEOUT = 1000

def load():
    """Returns the contents of the settings file as a string"""
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f) #wip: handle errors
    except FileNotFoundError:
        return []

def save(entries):
    """Saves the entry list `entries` to the settings file"""
    with open(SAVE_FILE, "w+") as f: #wip: handle errors
        json.dump(entries, f, indent = 4, separators=(",", ": "))

saved_entries = None
timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(lambda: save(saved_entries) if saved_entries != None else None)
def deferred_save(entries):
    timer.stop()
    global saved_entries
    saved_entries = entries
    timer.start(TIMEOUT)