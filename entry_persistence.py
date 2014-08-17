import os, json
from PySide import QtCore

SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reminders.json")
TIMEOUT = 3000

def load():
    """Returns the contents of the data file as a string"""
    try:
        with open(SAVE_FILE, "r") as f:
            value = json.load(f)
            print("Data file loaded.")
            return value
    except FileNotFoundError:
        print("Data file not found - using blank file.")
        return []
    except:
        print("Could not load data - exiting to avoid data loss.") #wip: print traceback
        exit(1)

def save(entries):
    """Saves the entry list `entries` to the data file"""
    try:
        with open(SAVE_FILE, "w+") as f:
            json.dump(entries, f, indent = 4, separators=(",", ": "))
            print("Data file saved.")
    except:
        print("Could not save file.") #wip: print traceback

saved_entries = None
timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(lambda: save(saved_entries) if saved_entries != None else None)
def deferred_save(entries):
    timer.stop()
    global saved_entries
    saved_entries = entries
    timer.start(TIMEOUT)
