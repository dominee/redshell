#! /usr/bin/env python
import os
from redshell.config import *
from datetime import datetime

# This is were we create a new project
project_dir = REDSHELL_REPORTS+os.sep+datetime.now().strftime("%Y"+os.sep+"%m"+os.sep+"%d")

def project_help():
    sys.stdout.write("""
[project]
Usage : project project-name

Used to create a new project folder and manage existing projects

Examples: 
project
project myNewProject
""")
    return SHELL_STATUS_RUN

def project_usage():
    sys.stdout.write("project project-name\n")
    return SHELL_STATUS_RUN

def project(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return project_help()
        if args[0] == 'usage':
            return project_usage()
        # If not anything above, than we use it as project name
        project_name = args[0]
        current_project_dir = project_dir+os.sep+project_name
    else:
        # TODO : return latest project dir
        return SHELL_STATUS_RUN    

    # Create a directory structure for the project
    if not os.path.isdir(current_project_dir):
        #os.makedirs(project_dir)
        sys.stdout.write("[ ] Creating new project folder:"+current_project_dir+"\n")

    return SHELL_STATUS_RUN

