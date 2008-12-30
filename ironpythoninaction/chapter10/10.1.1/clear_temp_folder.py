import os, stat
from datetime import datetime, timedelta

tempdir = os.environ["TEMP"]
max_age = datetime.now() - timedelta(7) 

for filename in os.listdir(tempdir):
    path = os.path.join(tempdir, filename)
    if os.path.isdir(path):
        continue
    mtime = datetime.fromtimestamp(os.stat(path).st_mtime) 
    if mtime < max_age:
        mode = os.stat(path).st_mode
        os.chmod(path, mode | stat.S_IWRITE)
        os.remove(path)
