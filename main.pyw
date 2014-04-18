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

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.conf")

def load():
    """Returns the contents of the settings file as a string"""
    with open(SETTINGS_FILE, "r") as f:
        return f.read()

def save(data):
    """Saves the string `data` to the settings file"""
    with open(SETTINGS_FILE, "w+") as f:
        f.write(data)

class InternalAPI(QtCore.QObject): #wip: save the state every so often on a delay
    def __init__(self, parent=None):
        super(InternalAPI, self).__init__(parent)

    @QtCore.Slot(int, str, result=int)
    def create(self, time, message):
        return 0 #wip: return the element ID

    @QtCore.Slot(int, result=None)
    def remove(self, entry):
        pass #wip

    @QtCore.Slot(int, int, bool, result=None)
    def time(self, entry, time, delete):
        pass #wip
    
    @QtCore.Slot(int, str, result=None)
    def message(self, entry, message):
        pass #wip

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