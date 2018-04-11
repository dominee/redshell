#! /usr/bin/env python
from stat import S_ISREG, ST_CTIME, ST_MODE
import os,time,glob

burp_dir = "/Users/dominee/pentest"

# get current working directory
start_dir = os.getcwd()

# cd into burp home so burp updates are downloaded there
os.chdir(burp_dir)
# filter out burp stable versions
burp_jars = glob.glob('burpsuite_pro_v*.jar')
# get stats for the files
entries = (os.path.join(burp_dir, fn) for fn in burp_jars)
entries = ((os.stat(path), path) for path in entries)
# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))
# get the newest one
ct,fp = sorted(entries,reverse=True)[0]

print '[ ] Using latest Burpsuite',fp,'(',time.ctime(ct),')'

# return to the directory we started from
os.chdir(start_dir)