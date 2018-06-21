#! /usr/bin/env python
import os
from redshell.config import *
from termcolor import colored

def TEMPLATE_help():
    sys.stdout.write("""
[TEMPLATE]
Usage : TEMPLATE [param1] <host>

This is just a TEMPLATE.

Examples: 
TEMPLATE param1 localhost
TEMPLATE localhost
""")
    return SHELL_STATUS_RUN

def TEMPLATE_usage():
    sys.stdout.write(colored("TEMPLATE","white")+" [param1] <host>\n")
    return SHELL_STATUS_RUN

def TEMPLATE(args):

    # Process arguments (inc. mandatory like 'help' and 'usage')    
    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return TEMPLATE_help()
        if args[0] == 'usage':
            return TEMPLATE_usage()

    # Main functionality
    sys.stdout.write("I am just a Template.\n")

    # Signal to exit subprocess
    return SHELL_STATUS_RUN

