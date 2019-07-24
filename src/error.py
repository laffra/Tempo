import datetime
import info
import log
import os
import platform
import rumps
import traceback

home_dir = os.path.join(os.path.expanduser("~"), "TempoApp")

def get_system_info():
    return """
System Details:

    Version:  %s
    Compiler: %s
    Build:    %s
    Platform: %s
    System:   %s
    Node:     %s
    Release:  %s
    Version:  %s

""" % (
        platform.python_version(),
        platform.python_compiler(),
        platform.python_build(),
        platform.platform(),
        platform.system(),
        platform.node(),
        platform.release(),
        platform.version(),
    )

def get_home_dir_info():
    return "\nTempo Home Folder:\n%s\n\n" % "\n".join([
        "    %s" % os.path.join(root, filename)
        for root, _, filenames in os.walk(home_dir)
        for filename in filenames
    ])

def get_preferences():
    try:
        import preferences
        import json
        if preferences.preferences:
            return "Tempo Preferences:\n%s\n\n" % json.dumps(preferences.preferences, indent=4)
    except:
        return ""

def get_versions():
    try:
        import version_manager
        return "Tempo Available Versions:\n%s\n\n" % version_manager.get_versions()
    except:
        return ""

def get_error_file_path():
    try:
        error_dir = os.path.join(os.path.join(home_dir, "errors"))
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        path = os.path.join(os.path.join(error_dir, "tempo_error-%s.txt" % datetime.datetime.utcnow()))
    except:
        path = os.path.join(os.path.expanduser("~"), "tempo_error.txt")
    return path.replace(' ', '_')

def error(message):
    stack = "Tempo Execution Stack at Error Time:\n%s\n" % "".join(traceback.format_stack()[:-1])
    exception = "Tempo Exception:\n    %s\n" % traceback.format_exc()
    error = "Tempo Error:\n    %s\n%s%s%s%s%s\n%s%sTempo Error:\n    %s\n" % (
        message,
        get_system_info(),
        get_home_dir_info(),
        get_preferences(),
        get_versions(),
        log.get_log(),
        stack,
        exception,
        message
    )
    path = get_error_file_path()
    try:
        with open(path, "w") as output:
            output.write("Tempo Error Report - %s\n\n" % datetime.datetime.utcnow())
        os.system("system_profiler SPHardwareDataType >> %s" % path)
        with open(path, "a") as output:
            output.write(error)
        with open(path) as input:
            print input.read()
    except:
        pass
    log.log("Running Tempo from %s" % __file__)
    log.log("Details: Version %s - by %s - %s" % (info.version, info.who, info.when))
    log.log(error)
    rumps.notification("Tempo", "Error: %s. For details see:" % message, path, sound=True)