import activity
import collections
import datetime
import error
import log
import os
import utils
import sqlite3
import webbrowser

title_details = {}

def get_activities():
    cursor = sqlite3.connect(activity.db_path()).cursor()
    return cursor.execute("SELECT * FROM activities").fetchall()

def get_report_path():
    reports_dir = os.path.join(utils.home_dir(), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return os.path.join(reports_dir, "report_%s.html" % datetime.datetime.utcnow())

def generate():
    try:
        filename = get_report_path()
        activities = get_activities()
        log.log("Generate report with %d events in file %s" % (len(activities), filename))
        with open(filename, "w") as output:
            generate_full_table(output, activities)
        webbrowser.open("file://%s" % filename)
    except:
        error.error("Cannot generate report")

def generate_full_table(output, activities):
    output.write("<table border=1 width=\"1400px\">")
    output.write("""
        <tr>
            <th>When</th>
            <th>CPU</th>
            <th>APP CPU</th>
            <th>User</th>
            <th>APP NAME</th>
            <th>Window/Tab Title</td>
            <th>FavIcon</th>
            <th>URL</th>
        </tr>""")

    for timestamp, cpu, app_cpu, user, pid, ppid, app_name, title, fav, url in activities:
        output.write(u"""
        <tr>
        <td>%s</td>
        <td>%d%%</td>
        <td>%d%%</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        """ % (
            datetime.datetime.fromtimestamp(timestamp),
            int(cpu * 100),
            int(app_cpu * 100),
            user,
            app_name,
            title.encode('ascii', 'ignore')[:100],
            u'<img src="%s" width=28>' % fav if fav else "",
            u'<a target=_blank href="%s">url</a>' % url if url else "",
        ))
    output.write("</table>")
