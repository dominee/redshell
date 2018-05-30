#! /usr/bin/env python
import ConfigParser
import os
import sys
from redshell.constants import *

# Set default values
REDSHELL_DIR = os.path.expanduser(DEFAULT_REDSHELL_DIR)
REDSHELL_HISTORY = os.path.expanduser(DEFAULT_REDSHELL_HISTORY)
REDSHELL_REPORTS = os.path.expanduser(DEFAULT_REDSHELL_REPORTS)
REDSHELL_NMAP = DEFAULT_REDSHELL_NMAP
REDSHELL_SUDO = DEFAULT_REDSHELL_SUDO
REDSHELL_UA = DEFAULT_REDSHELL_UA
REDSHELL_PROXY = DEFAULT_REDSHELL_PROXY

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

    # Create subfolders in the homedir. if they exist just skip
    try:    
        for subdir in REDSHELL_DIR_SUBDIRS:
            os.makedirs(REDSHELL_DIR+os.sep+subdir)
    except:
        pass

# If no entry exists in config file or is not valid just ignore it    
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
    # If the path does not exist, create it and use it
    if not os.path.isdir(redshell_reports_conf):
        try:
            os.makedirs(redshell_reports_conf)
        except:
            sys.stdout.write("Unable to create report directory: %s. Using default path: %s" % (redshell_reports_conf,DEFAULT_REDSHELL_REPORTS))
        else:
            REDSHELL_REPORTS = redshell_reports_conf    
    else:
        REDSHELL_REPORTS = redshell_reports_conf
# If no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Bin / nmap : binary for nmap
# Check if a value is provided in config file
try:
    redshell_nmap_conf = os.path.expanduser(ConfigSectionMap("Bin")['nmap'])
    if os.path.isfile(redshell_nmap_conf) and os.access(redshell_nmap_conf, os.X_OK):
        REDSHELL_NMAP = redshell_nmap_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Bin / sudo : binary for sudo
# Check if a value is provided in config file
try:
    redshell_sudo_conf = os.path.expanduser(ConfigSectionMap("Bin")['sudo'])
    if os.path.isfile(redshell_sudo_conf) and os.access(redshell_sudo_conf, os.X_OK):
        REDSHELL_SUDO = redshell_sudo_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Bin / dig : binary for dig
# Check if a value is provided in config file
try:
    redshell_dig_conf = os.path.expanduser(ConfigSectionMap("Bin")['dig'])
    if os.path.isfile(redshell_dig_conf) and os.access(redshell_dig_conf, os.X_OK):
        REDSHELL_DIG = redshell_dig_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass
    
    
## CONFIG: Web / proxy : web proxy
# Check if a value is provided in config file
try:
    redshell_proxy_conf = ConfigSectionMap("Web")['proxy']
    if redshell_proxy_conf:
        REDSHELL_PROXY = redshell_proxy_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

## CONFIG: Web / UA : web UA
# Check if a value is provided in config file
try:
    redshell_ua_conf = ConfigSectionMap("Web")['user-agent']
    if redshell_ua_conf:
        REDSHELL_UA = redshell_ua_conf
# if no entry exists in config file or is not valid just ignore it    
except: 
    pass

