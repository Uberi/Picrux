#!/usr/bin/python

# TODO:
# * save the contents of the search box and serialized entries
# * make entirely keyboard operable
# * Vim keybindings

# standard library modules
import os, sys

# external modules
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtDeclarative import QDeclarativeView

# internal modules
import entry_persistence

class InternalAPI(QtCore.QObject): #wip: save the state every so often on a delay
    def __init__(self, parent=None):
        super(InternalAPI, self).__init__(parent)
        self.entries = entry_persistence.load()
        self.index = 0

    @QtCore.Slot(int, str, result=str)
    def create(self, time, message, has_time):
        self.entries.append({"index": self.index, "time": time if has_time else None, "message": message})
        self.index += 1
        entry_persistence.deferred_save(self.entries)
        return self.index

    @QtCore.Slot(int, result=None)
    def remove(self, entry_index):
        self.entries = [entry for entry in self.entries if entry["index"] != entry_index]
        entry_persistence.deferred_save(self.entries)

    @QtCore.Slot(int, int, bool, result=None)
    def time(self, entry_index, time, delete):
        entry = next((entry for entry in self.entries if entry["index"] == entry_index), {}) #wip: handle nonexistant indices
        entry["time"] = None if delete else time
        entry_persistence.deferred_save(self.entries)

    @QtCore.Slot(int, str, result=None)
    def message(self, entry_index, message):
        entry = next((entry for entry in self.entries if entry["index"] == entry_index), {}) #wip: handle nonexistant indices
        entry["message"] = message
        entry_persistence.deferred_save(self.entries)

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