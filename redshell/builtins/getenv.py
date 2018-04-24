import os,sys
from redshell.constants import *

def getenv_usage():
    sys.stdout.write("getenv\n")
    return SHELL_STATUS_RUN

def getenv_help():
    sys.stdout.write("""
[getenv]
Usage : getenv <variable>

Get OS environment variable.

Example:
getenv PATH

""")
    return SHELL_STATUS_RUN

def getenv(args):
    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'usage':
            return getenv_usage()
        if args[0] == 'help':
            return getenv_help()
        sys.stdout.write(os.getenv(args[0])+"\n")
    else:
        sys.stdout.write("Variable name required.\n")
    return SHELL_STATUS_RUN
