import error
import imp
import log
import os
import requests
import zipfile
import StringIO
import sys

LATEST_URL = "https://github.com/laffra/Tempo/raw/master/latest_dist.zip"

home_dir = os.path.join(os.path.expanduser("~"), "TempoApp")
downloads_dir = os.path.join(home_dir, "src")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)


def setup():
    if not getattr(sys, "_MEIPASS", False):
        # running locally, so do not run latest version
        return
    try:
        r = requests.get(LATEST_URL, stream=True)
        log.log("Download latest version from " % LATEST_URL)
        zipfile.ZipFile(StringIO.StringIO(r.content)).extractall(downloads_dir)
        log.log("Set sys path to %s" % downloads_dir)
        sys.path.insert(0, downloads_dir)
    except Exception as e:
        error.error("ERROR: Could not download latest version due to %s" % e)

def run():
    try:
        __import__("latest").run()
    except Exception as e:
        error.error("Could not run tempo/main: %s" % e)

def main():
    setup()
    run()

if __name__ == "__main__":
    main()
