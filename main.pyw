#!/usr/bin/python

# TODO:
# * save the contents of the search box and serialized entries
# * make entirely keyboard operable
# * Vim keybindings

# standard library modules
import os, sys
import json

# external modules
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtDeclarative import QDeclarativeView

SAVE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reminders.json")

def load():
    """Returns the contents of the settings file as a string"""
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f) #wip: handle errors
    except FileNotFoundError:
        return []

def save(entries):
    """Saves the entry list `entries` to the settings file"""
    with open(SAVE_FILE, "w+") as f:
        json.dump(entries, indent = 4, separators=(",", ": "))

class InternalAPI(QtCore.QObject): #wip: save the state every so often on a delay
    def __init__(self, parent=None):
        super(InternalAPI, self).__init__(parent)
        self.entries = load()
        self.index = 0

    @QtCore.Slot(int, str, result=str)
    def create(self, time, message, has_time):
        self.entries.append({"index": self.index, "time": time if has_time else None, "message": message})
        self.index += 1
        return self.index

    @QtCore.Slot(int, result=None)
    def remove(self, entry_index):
        self.entries = [entry for entry in self.entries if entry["index"] != entry_index]

    @QtCore.Slot(int, int, bool, result=None)
    def time(self, entry_index, time, delete):
        entry = next((entry for entry in self.entries if entry["index"] == entry_index), {}) #wip: handle nonexistant indices
        entry["time"] = None if delete else time

    @QtCore.Slot(int, str, result=None)
    def message(self, entry_index, message):
        entry = next((entry for entry in self.entries if entry["index"] == entry_index), {}) #wip: handle nonexistant indices
        entry["message"] = message

class PicruxWindow:
    def __init__(self):
        self.load_fonts()

        # set up window
        self.view = QtWebKit.QWebView()
        api = InternalAPI()
        self.view.page().mainFrame().addToJavaScriptWindowObject("_server_side_", api)
        self.view.load(QtCore.QUrl("views/main.html"))
        self.view.setWindowTitle("Picrux v0.3")
        self.view.setWindowIcon(QtGui.QIcon("icon.png"))
        self.view.show()

        # center window on screen
        position = self.view.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        position.moveCenter(center)
        self.view.move(position.topLeft())

    def load_fonts(self):
        """Load font without installing in system"""
        for path in os.listdir("fonts"):
            path = os.path.join("fonts", path)
            if os.path.isfile(path):
                QtGui.QFontDatabase.addApplicationFont(path)

if __name__ == "__main__":
    # start application
    application = QtGui.QApplication(sys.argv)
    window = PicruxWindow()
    sys.exit(application.exec_())