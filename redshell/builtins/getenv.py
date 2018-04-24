import os,sys
from redshell.constants import *

def getenv_usage():
    sys.stdout.write("getenv\n")
    return SHELL_STATUS_RUN

def getenv(args):
    # Do we need to display usage or help?
    if args[0] == 'usage':
        return getenv_usage()

    if len(args) > 0:
        sys.stdout.write(os.getenv(args[0]))
    return SHELL_STATUS_RUN
