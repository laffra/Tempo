import os

EXTENSION_ID = "aplkeadhbiimpoggemmejeiiimpmijgd"
EXTENSION_PATH = "~/Library/Application Support/Google/Chrome/External Extensions/"

def install():
  dir = os.path.expanduser(EXTENSION_PATH)
  path = os.path.join(dir, "%s.json" % EXTENSION_ID)
  if not os.path.exists(path):
    if not os.path.exists(dir):
      os.makedirs(dir)
    with open(path, "w") as fout:
      fout.write("""
{
  "external_update_url": "https://clients2.google.com/service/update2/crx",
  "external_version": "1.0"
}
""")
  print("installed extension in %s" % path)