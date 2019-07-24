import activity
import info
import error
import extension
import functools
import gc
import install
import log
import os
import preferences
import process
import profiler
import rumps
import server
import sys
import time
import utils
import webbrowser

RESOURCE_PATH = getattr(sys, "_MEIPASS", os.path.abspath("."))
ICON = os.path.join(RESOURCE_PATH, "icons/tempo-icon.png")

TITLE_QUIT = "Quit Tempo"
TITLE_REPORT = "Show Activity Report..."
TITLE_ABOUT = "About Tempo - %s"

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
        log.log("Started Tempo")

    def report(self, menuItem=None):
        try:
            server.load_report()
            # profiler.dump_stats()
        except:
            error.error("Error in menu callback")
        finally:
            self.handle_action()

    def version(self):
        return "latest"

    def update(self):
        activity.update_current_process()

    def create_menu(self):
        self.icon = ICON
        self.title = ""
        self.menu.clear()
        self.menu = [
            rumps.MenuItem(TITLE_ABOUT % self.version(), callback=self.about),
            None,
            rumps.MenuItem(TITLE_REPORT, callback=self.report),
            None,
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
        webbrowser.open("https://github.com/laffra/Tempo")

    def handle_action(self, menuItem=None):
        if menuItem:
            log.log("Handled menu item %s" % menuItem)


def run(quit_callback=None):
    log.log("Running Tempo from %s" % __file__)
    log.log("Details: Version %s - by %s - %s" % (info.version, info.who, info.when))
    log.log("Python system path:")
    for n, p in enumerate(sys.path):
        log.log("  %d  %s" % (n,p))
    extension.install()
    rumps.notification("Tempo", "Tempo is now running", "See the T icon in the status bar", sound=False)
    TempoStatusBarApp(quit_callback).run()
