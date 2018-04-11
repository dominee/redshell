#! /usr/bin/env python
import ConfigParser
import os
import sys
from redshell.constants import *

# set default values
REDSHELL_DIR = os.path.expanduser(DEFAULT_REDSHELL_DIR)
REDSHELL_HISTORY = os.path.expanduser(DEFAULT_REDSHELL_HISTORY)
REDSHELL_REPORTS = os.path.expanduser(DEFAULT_REDSHELL_REPORTS)

REDSHELL_DIR_SUBDIRS = ['log','output','lists','tools']

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

try:
    Config = ConfigParser.ConfigParser()
    if os.path.isfile(os.path.expanduser('~'+os.sep+'redshell.conf')):
        Config.read("redshell.conf")
    else:
        if os.path.isfile("redshell.conf"):    
            Config.read("redshell.conf")
except:
    pass

## CONFIG: Paths / redshell : Redshell Home directory
# Check if a value is provided in config file
try:
    redshell_dir_conf = os.path.expanduser(ConfigSectionMap("Paths")['redshell'])
    # if the path does not exist, create it and use it
    if not os.path.isdir(redshell_dir_conf):
        try:
            os.makedirs(redshell_dir_conf)
        except:
            sys.stdout.write("Unable to create home directory: %s. Using default path: %s" % (redshell_dir_conf,DEFAULT_REDSHELL_DIR))
        else:
            REDSHELL_DIR = redshell_dir_conf    
    else:
        REDSHELL_DIR = redshell_dir_conf

    # create subfolders in the homedir. if they exist just skip
    try:    
        for subdir in REDSHELL_DIR_SUBDIRS:
            os.makedirs(REDSHELL_DIR+os.sep+subdir)
    except:
        pass

# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Paths / history : Redshell history file
# Check if a value is provided in config file
try:
    redshell_history_conf = os.path.expanduser(ConfigSectionMap("Paths")['history'])
    if os.path.isfile(redshell_history_conf):
        REDSHELL_HISTORY = redshell_history_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Paths / report : Redshell directory for reports
# Check if a value is provided in config file
try:
    redshell_reports_conf = os.path.expanduser(ConfigSectionMap("Paths")['reports'])
    # if the path does not exist, create it and use it
    if not os.path.isdir(redshell_reports_conf):
        try:
            os.makedirs(redshell_reports_conf)
        except:
            sys.stdout.write("Unable to create report directory: %s. Using default path: %s" % (redshell_reports_conf,DEFAULT_REDSHELL_REPORTS))
        else:
            REDSHELL_REPORTS = redshell_reports_conf    
    else:
        REDSHELL_REPORTS = redshell_reports_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

#debug
#print("REDSHELL_DIR: ", REDSHELL_DIR)
#print("REDSHELL_HISTORY: ", REDSHELL_HISTORY)
#print("REDSHELL_REPORTS: ", REDSHELL_REPORTS)