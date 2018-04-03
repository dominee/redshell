import os
from redshell.constants import *


def getenv(args):
    if len(args) > 0:
        print(os.getenv(args[0]))
    return SHELL_STATUS_RUN
