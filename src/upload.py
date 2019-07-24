import shutil

import os


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "latest_dist")
    shutil.make_archive(path, 'zip', "src/latest")