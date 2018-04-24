#! /usr/bin/env python
from stat import S_ISREG, ST_CTIME, ST_MODE
import os,time,glob
from redshell.config import *
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

burp_dir = REDSHELL_DIR+os.sep+'tools'+os.sep+'burp'
burp_log = REDSHELL_DIR+os.sep+'log'+os.sep+datetime.now().strftime(os.sep+"%Y"+os.sep+"%m"+os.sep+"%d")

def burp_help():
    sys.stdout.write("""
[burp]
Usage : burp

Wrapper for burp to add auto-logging of console output. It starts the newst jar file from BURP_DIR.

""")
    return SHELL_STATUS_RUN

def burp_usage():
    sys.stdout.write("burp\n")
    return SHELL_STATUS_RUN

def burp(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return burp_help()
        if args[0] == 'usage':
            return burp_usage()

    # Get current working directory
    start_dir = os.getcwd()

    # Cd into burp home so burp updates are downloaded there
    if not os.path.isdir(burp_dir):
        os.mkdir(burp_dir)
    else:    
        os.chdir(burp_dir)

    # Create log dir for today
    if not os.path.isdir(burp_log):
        os.makedirs(burp_log)

    # Filter out burp stable versions
    burp_jars = glob.glob('burpsuite_pro_v*.jar')
    # Get stats for the files
    entries = (os.path.join(burp_dir, fn) for fn in burp_jars)
    entries = ((os.stat(path), path) for path in entries)
    # Leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    # Get the newest one
    ct,fp = sorted(entries,reverse=True)[0]

    print '[ ] Using latest Burpsuite',fp,'(',time.ctime(ct),')'

    # Open a new logfile with timestamp suffix and run burp
    logfile = open(burp_log+os.sep+"burp-console-"+datetime.now().strftime("%H%M%S")+".log", 'ab')
    try:
        p = Popen(['java', '-jar', '-Xmx4g', '-XX:MaxPermSize=2G', fp], stdout=logfile, stderr=STDOUT, cwd=burp_dir, bufsize=1)
        sys.stdout.write("[+] Burpsuite starting [%s]\n" % p.pid)
    except:
        sys.stdout.write("[!] Error: "+sys.exc_info()[0])

    # Return to the directory we started from
    os.chdir(start_dir)

    return SHELL_STATUS_RUN