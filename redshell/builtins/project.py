#! /usr/bin/env python
import os
from redshell.config import *
from datetime import datetime
from distutils import dir_util
from termcolor import colored

# TODO : return path to latest project and or cd

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
    sys.stdout.write(colored("project","white")+" project-name\n")
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
        sys.stdout.write(STAR+"Creating new project folder: "+colored(current_project_dir,'white')+"\n")
        os.makedirs(project_dir)
        sys.stdout.write(LS+"Populating with templates... ")
        templates = dir_util.copy_tree(REDSHELL_TEMPLATES,current_project_dir,dry_run=0)
        sys.stdout.write("( "+str(len(templates))+" files )\n")

        # TODO: create symlinks to wordlists (for burp)?
        # TODO: touch file placeholders for burpproject etc, to have a consistent naming policy

    else:
        sys.stdout.write(EX+"Such project already exists : "+colored(current_project_dir,'white')+"\n")

    return SHELL_STATUS_RUN

