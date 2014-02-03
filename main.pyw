#!/usr/bin/python

# TODO:
# * save the contents of the search box and serialized entries

# standard library modules
import os, sys, time
import http.server
from urllib.parse import urlparse, unquote
from datetime import datetime

# external modules
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtDeclarative import QDeclarativeView

# bundled modules
from dateutil import rrule
import recurrent

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.conf")

def load():
    """Returns the contents of the settings file as a string"""
    with open(SETTINGS_FILE, "r") as f:
        return f.read()

def save(data):
    """Saves the string `data` to the settings file"""
    with open(SETTINGS_FILE, "w+") as f:
        f.write(data)

class InternalAPI(QtCore.QObject):
    def __init__(self, parent=None):
        super(InternalAPI, self).__init__(parent)

    @QtCore.Slot(str, result=str)
    def parse_time(self, message):
        if not message:
            return ""
        occurrence = recurrent.RecurringEvent().parse(message)
        if occurrence == None:
            return ""
        if isinstance(occurrence, str):
            occurrence = rrule.rrulestr(occurrence).after(datetime.now(), True)
        unix_time = time.mktime(occurrence.utctimetuple())
        return str(unix_time)

class PicruxWindow:
    def __init__(self):
        self.load_fonts()

        # set up window
        self.view = QtWebKit.QWebView()
        api = InternalAPI()
        self.view.page().mainFrame().addToJavaScriptWindowObject("_python_side_", api)
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