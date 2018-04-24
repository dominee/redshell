#! /usr/bin/env python
import os
from redshell.config import *
from subprocess import Popen, STDOUT
from datetime import datetime

nmap_dir = REDSHELL_DIR+os.sep+'tools'+os.sep+'nmap'
nmap_log = REDSHELL_DIR+os.sep+'log'+os.sep+datetime.now().strftime("%Y"+os.sep+"%m"+os.sep+"%d")

nmap_args = ['-v',                  # Verbose
            '-Pn',                  # Treat all hosts as online -- skip host discovery
            '--data-length','32',   # Append random data to sent packets
            ]

def nmap_help():
    sys.stdout.write("""
[nmap]
Usage : nmap [sudo] <nmap arguments> <host>

Wrapper for nmap to add auto-logging and some auto-include switches.

Examples: 
nmap -p 22 localhost
nmap sudo -sS -p 22 localhost
""")
    return SHELL_STATUS_RUN

def nmap_usage():
    sys.stdout.write("nmap [sudo] <nmap arguments> <host>\n")
    return SHELL_STATUS_RUN

def nmap(args):
    
    # Create log dir for today
    if not os.path.isdir(nmap_log):
        os.makedirs(nmap_log)

    if len(args) > 0:
        # Do we need to run it privileged?
        if args[0] == 'sudo':
            args.pop(0)
            sudo=True
        else:
            sudo=False
        # Do we need to display usage or help?
        if args[0] == 'help':
            return nmap_help()
        if args[0] == 'usage':
            return nmap_usage()

    nmap_log_file = nmap_log+os.sep+'nmap'+'_'.join(args)+'-'+datetime.now().strftime("%H%M%S")

    try:
        if not sudo:
            p = Popen([REDSHELL_NMAP, '-oA', nmap_log_file]+args, bufsize=1)
            sys.stdout.write("[+] Nmap starting [%s]\n" % p.pid)
        else:
            # For now we asume that nmap is in sudeoers passwordless ;p
            # user ALL = (root) NOPASSWD: /usr/local/bin/nmap
            # TODO: use pexpect
            p = Popen([REDSHELL_SUDO, REDSHELL_NMAP, '-oA', nmap_log_file+' ']+args, bufsize=1, shell=False)
            sys.stdout.write("[+] (sudo) Nmap starting [%s]\n" % p.pid)
    except:
        sys.stdout.write("[!] Error: "+sys.exc_info()[0])
    return SHELL_STATUS_RUN

