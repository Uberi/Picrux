#!/usr/bin/python

# TODO:
# * save the contents of the search box and serialized entries

# standard library modules
import os, sys, time
import http.server
from urllib.parse import urlparse, unquote
import threading
from datetime import datetime

# external modules
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtDeclarative import QDeclarativeView

# bundled modules
from dateutil import rrule
import recurrent

SERVER_ADDRESS = ("localhost", 222)
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.conf")

def parse_time(message):
    if not message:
        return ""
    occurrence = recurrent.RecurringEvent().parse(message)
    if occurrence == None:
        return ""
    if isinstance(occurrence, str):
        occurrence = rrule.rrulestr(occurrence).after(datetime.now(), True)
    unix_time = time.mktime(occurrence.utctimetuple())
    return str(unix_time)

def load():
    """Returns the contents of the settings file as a string"""
    with open(SETTINGS_FILE, "r") as f:
        return f.read()

def save(data):
    """Saves the string `data` to the settings file"""
    with open(SETTINGS_FILE, "w+") as f:
        f.write(data)

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

    def load_fonts(self):
        """Load font without installing in system"""
        for path in os.listdir("fonts"):
            path = os.path.join("fonts", path)
            if os.path.isfile(path):
                QtGui.QFontDatabase.addApplicationFont(path)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): # avoid logging everything to stdout
        pass

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path, data = parsed_url.path, unquote(parsed_url.query)
        if path == "/parse_time":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            time = parse_time(data)
            self.wfile.write(bytes(time, "utf-8"))
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