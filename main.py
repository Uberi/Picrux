#!/usr/bin/python

# TODO:
# * save the contents of the search box and serialized entries

# standard library modules
import os, sys
import http.server
import threading

# external modules
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtDeclarative import QDeclarativeView

SERVER_ADDRESS = ("localhost", 222)
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.conf")

class PicruxWindow:
    def __init__(self):
        self.load_fonts()

        # set up window
        self.view = QtWebKit.QWebView()
        self.view.load(QtCore.QUrl("views/main.html"))
        self.view.setWindowTitle("Picrux v0.2")
        self.view.setWindowIcon(QtGui.QIcon("icon.png"))
        self.view.show()

        # center window on screen
        position = self.view.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        position.moveCenter(center)
        self.view.move(position.topLeft())

    def load(self):
        """Returns the contents of the settings file as a string"""
        with open(SETTINGS_FILE, "r") as f:
            return f.read()

    def save(self, data):
        """Saves the string `data` to the settings file"""
        with open(SETTINGS_FILE, "w+") as f:
            f.write(data)

    def load_fonts(self):
        """Load font without installing in system"""
        for path in os.listdir("fonts"):
            path = os.path.join("fonts", path)
            if os.path.isfile(path):
                QtGui.QFontDatabase.addApplicationFont(path)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass

    def do_GET(self):
        if self.path == "/parse_time":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes("{\"x\":1}", "utf-8"))
        else:
            self.send_error(404, "Page \"%s\" not found" % self.path)

    def do_POST(self):
        pass

def run_server():
    httpd = http.server.HTTPServer(SERVER_ADDRESS, RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    # start server
    server = threading.Thread(target=run_server, daemon=True)
    server.start()

    # start application
    application = QtGui.QApplication(sys.argv)
    window = PicruxWindow()
    sys.exit(application.exec_())