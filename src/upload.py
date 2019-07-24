import os
import shutil
import sys
from datetime import date

def createLatestZip():
    srcDir = os.path.dirname(__file__)
    infoPath = os.path.join(srcDir, "info.py")

    with open(infoPath) as fin:
        print("Current version:\n")
        print("=" * 90)
        print(fin.read())
        print("=" * 90)
        print()

    version = raw_input("What version do you want to publish? ")
    yesno = raw_input("Generate zip for version %s (Y/N)? " % version)
    if (yesno in ["Y", "y"]):
        with open(infoPath, "w") as fout:
            fout.write("version = '%s'\n" % version)
            fout.write("when = '%s'\n" % date.today())
            fout.write("who = '%s'\n" % os.path.expanduser("~").replace("/Users/", ""))

        rootDir = os.path.dirname(srcDir)
        zipPath = os.path.join(rootDir, "latest_dist")
        shutil.make_archive(zipPath, 'zip', "src/latest")

        print("Created latest zip in %s.zip:" % zipPath)
        os.system("unzip -v %s.zip" % zipPath)
        print("Next step: commit and push")


if __name__ == "__main__":
    createLatestZip()