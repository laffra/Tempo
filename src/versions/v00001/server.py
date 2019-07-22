import activity
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import log
import os
import sys
import threading
import urlparse
import webbrowser

port_number = 1187
reload(sys)
sys.setdefaultencoding('utf-8')

HTML_PATH = os.path.join(os.path.dirname(__file__), "html")
FILES = {
    "/index": ("index.html", "text/html"),
    "/calendar": ("calendar.html", "text/html"),
    "/calendar.css": ("calendar.css", "text/css"),
    "/calendar.js": ("calendar.js", "application/javascript"),
    "/d3pie.js": ("d3pie.js", "application/javascript"),
    "/favicon.ico": ("favicon.ico", "image/x-icon")
}

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/tempo?"):
            query = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            url = query.get('url', [''])[0]
            title = query.get('title', [''])[0]
            email = query.get('email', [''])[0]
            fav = query.get('fav', [''])[0]
            activity.update_tab(email, fav, title, url)
        elif self.path in FILES:
            self.send_file(*FILES[self.path])
        elif self.path.startswith("/events?"):
            query = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            start = query.get('start')[0]
            end = query.get('end')[0]
            self.send_json(activity.get_activities(start, end))
        else:
            log.log("SERVER - NOT FOUND: %s" % self.path)

    def send_json(self, object):
        self.respond("application/json")
        self.wfile.write(json.dumps(object))

    def send_csv(self, rows):
        self.respond("text/csv")
        self.wfile.write("\n".join(",".join(map(str, row)) for row in rows))

    def send_file(self, path, type):
        with open(os.path.join(HTML_PATH, path), "rb") as fin:
            self.respond(type)
            self.wfile.write(fin.read())

    def respond(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def log_message(self, format, *args):
        return

class Runner(threading.Thread):
    def run(self):
        global port_number
        while True:
            try:
                log.log("Start server on port number %d" % port_number)
                HTTPServer(('', port_number), Server).serve_forever()
            except Exception as e:
                log.log("Port number %d already in use: %s" % (port_number, e))
                port_number += 1

def load_report():
    webbrowser.open("http://localhost:%d/index" % port_number)


def start_server():
    log.log("Start the server")
    Runner().start()
