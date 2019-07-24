import error
import imp
import log
import os
import requests
import zipfile
import StringIO
import sys

LATEST_URL = "https://github.com/laffra/Tempo/raw/master/archives/latest_dist.zip"

home_dir = os.path.join(os.path.expanduser("~"), "TempoApp")
downloads_dir = os.path.join(home_dir, "src")
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

running_local = not getattr(sys, "_MEIPASS", False)

def setup():
    if running_local:
        log.log("Running Tempo locally. Do not download and run latest version")
        return
    try:
        r = requests.get(LATEST_URL, stream=True)
        log.log("Download latest version from %s" % LATEST_URL)
        zipfile.ZipFile(StringIO.StringIO(r.content)).extractall(downloads_dir)
        log.log("Set sys path to %s" % downloads_dir)
        sys.path.insert(0, downloads_dir)
    except Exception as e:
        error.error("ERROR: Could not download latest version due to %s" % e)

def run():
    try:
        __import__("main").run()  # use the latest downloaded version
    except:
        try:
            __import__("latest").run()  # use the development version
        except Exception as e:
            error.error("Could not run tempo/main: %s" % e)

def main():
    setup()
    run()

if __name__ == "__main__":
    main()
