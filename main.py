#!/usr/bin/python

# TODO:
# * set up a simple webserver to communicate with JS
# * save the contents of the search box and serialized entries

import os, sys
from PySide import QtCore, QtGui
from PySide.QtDeclarative import QDeclarativeView
from PySide.QtWebKit import *

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.conf")

class PicruxWindow:
    def __init__(self):
        self.load_fonts()
        
        # set up window
        self.view = QWebView()
        self.view.load(QtCore.QUrl("views/main.html"))
        self.view.setWindowTitle("Picrux v0.2")
        self.view.setWindowIcon(QtGui.QIcon("icon.png"))
        self.view.show()
        
        # center window on screen
        position = self.view.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        position.moveCenter(center)
        self.view.move(position.topLeft())

    def load():
        """Returns the contents of the settings file as a string"""
        with open(SETTINGS_FILE, "r") as f:
            return f.read()

    def save(data):
        """Saves the string `data` to the settings file"""
        with open(SETTINGS_FILE, "w+") as f:
            f.write(data)

    def load_fonts(self):
        """Load font without installing in system"""
        for path in os.listdir("fonts"):
            path = os.path.join("fonts", path)
            if os.path.isfile(path):
                QtGui.QFontDatabase.addApplicationFont(path)

if __name__ == "__main__":
    application = QtGui.QApplication(sys.argv)
    window = PicruxWindow()
    sys.exit(application.exec_())
