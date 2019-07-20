import activity
import error
import extension
import functools
import gc
import install
import license
import log
import os
import preferences
import process
import profiler
import report
import rumps
import server
import suspender
import sys
import time
import utils
import version_manager
import webbrowser

RESOURCE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
ICON = os.path.join(RESOURCE_PATH, "icons/tempo-icon.png")

TITLE_QUIT = "Quit Tempo"
TITLE_REPORT = "Show Activity Report..."
TITLE_ABOUT = "About Tempo - %s"

running_local = not getattr(sys, "_MEIPASS", False)

class TempoStatusBarApp(rumps.App):
    def __init__(self, quit_callback=None):
        super(TempoStatusBarApp, self).__init__("", quit_button=None)
        self.quit_button = None
        self.quit_callback = quit_callback
        self.menu = []
        self.create_menu()
        self.start = time.time()
        self.menu_is_open = False
        server.start_server()
        utils.Timer(2, self.update).start()
        log.log("Started Tempo %s" % version_manager.last_version())

    def report(self, menuItem=None):
        try:
            report.generate()
            profiler.dump_stats()
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def version(self):
        return version_manager.last_version()

    def update(self):
        activity.update_current_process()

    def create_menu(self):
        self.icon = ICON
        self.title = ""
        self.menu.clear()
        report = [rumps.MenuItem(TITLE_REPORT, callback=self.report), None] if running_local else []
        self.menu = [
            rumps.MenuItem(TITLE_ABOUT % self.version(), callback=self.about),
            None,
        ] + report + [
            rumps.MenuItem(TITLE_QUIT, callback=self.quit),
        ]
        self.menu._menu.setDelegate_(self)

    def menuWillOpen_(self, menu):
        self.menu_is_open = True

    def menuDidClose_(self, menu):
        self.menu_is_open = False

    def quit(self, menuItem=None):
        rumps.quit_application()

    def about(self, menuItem=None):
        webbrowser.open("http://happymac.app")

    def handle_action(self, menuItem=None):
        if menuItem:
            log.log("Handled menu item %s" % menuItem)


def run(quit_callback=None):
    if license.get_license():
        extension.install()
        rumps.notification("Tempo", "Tempo is now running", "See the emoji icon in the status bar", sound=False)
        TempoStatusBarApp(quit_callback).run()
