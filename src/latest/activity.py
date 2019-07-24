import collections
import error
import log
import os
import process
import re
import sqlite3
import time
import utils
import webbrowser

DB_FILE_NAME = "activities.db"
DORMANT_PROCESS_CPU = 0.01
INIT_QUERY = """CREATE TABLE IF NOT EXISTS activities (
    timestamp float,
    system float,
    cpu float,
    user text,
    pid text,
    ppid text,
    name text,
    title text,
    fav text,
    url text
) """

INDEX_TIMESTAMP = 0
INDEX_SYSTEM = 1
INDEX_CPU = 2
INDEX_USER = 3
INDEX_PID = 4
INDEX_PPID = 5
INDEX_APP_NAME = 6
INDEX_TITLE = 7
INDEX_FAV = 8
INDEX_URL = 9

HOUR_IN_MS = 3600 * 1000000

Activity = collections.namedtuple("Activity", ["timestamp", "system", "cpu", "user", "pid", "ppid", "name", "title", "fav", "url"])
VisitedTab = collections.namedtuple("Tab", ["user", "fav", "title", "url"])
last_tab = VisitedTab("", "", "", "")
chrome_users = {}

def db_path():
    home_dir = utils.home_dir()
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    return os.path.join(home_dir, DB_FILE_NAME)

def get_activities(start, end):
    cursor = sqlite3.connect(db_path()).cursor()
    query = "SELECT * FROM activities WHERE timestamp > %s AND timestamp < %s" % (start, end)
    return cursor.execute(query).fetchall()

def update_tab(user, fav, title, url):
    global last_tab
    last_tab = VisitedTab(user, unicode(fav), unicode(title), unicode(url))
    chrome_users[utils.get_active_window_number()] = user
    update_current_process()

def update_current_process():
    pid = utils.get_current_app_pid()
    cpu = process.cpu(pid)
    if cpu < DORMANT_PROCESS_CPU:
        return
    app_name = utils.get_current_app_name()
    if app_name == "Google Chrome":
        user, fav, title, url = last_tab
        user = chrome_users.get(utils.get_active_window_number(), user)
    else:
        user, fav, title, url = (process.get_owner(pid), "", utils.get_active_window_name(), "")
    save_event(
        int(time.time()),
        process.cpu(-1),
        cpu,
        unicode(user),
        pid,
        process.parent_pid(pid),
        app_name,
        title,
        fav,
        url
    )
    return "%s %s" % (user, app_name)

def save_event(timestamp, system, cpu, user, pid, ppid, name, title, fav, url):
    # log.log("event %s %s %s" % (cpu, name, user))
    connection = sqlite3.connect(db_path())
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO activities (
                timestamp,
                system,
                cpu,
                user,
                pid,
                ppid,
                name,
                title,
                fav,
                url)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, [ timestamp, system, cpu, user, pid, ppid, name, title, fav, url ]
    )
    connection.commit()

def setup():
    sqlite3.connect(db_path()).cursor().execute(INIT_QUERY)

try:
    setup()
except Exception as e:
    log.log("Cannot open activity database: %s. Retrying..." % e)
    os.system("mv %s %s.%s" % (db_path(), db_path(), time.time()))
    try:
        setup()
    except:
        error.error("Cannot initialize activities.")
