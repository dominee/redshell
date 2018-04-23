#! /usr/bin/env python
import os
from redshell.config import *
from subprocess import Popen, STDOUT
from datetime import datetime

nmap_dir = REDSHELL_DIR+os.sep+'tools'+os.sep+'nmap'
nmap_log = REDSHELL_DIR+os.sep+'log'+os.sep+datetime.now().strftime("%Y"+os.sep+"%m"+os.sep+"%d")

def nmap(args):
    
    # create log dir for today
    if not os.path.isdir(nmap_log):
        os.makedirs(nmap_log)

    if args[0] == 'sudo':
        args.pop(0)
        sudo=True
    else:
        sudo=False

    nmap_log_file = nmap_log+os.sep+'nmap'+'_'.join(args)+'-'+datetime.now().strftime("%H%M%S")

    try:
        if not sudo:
            p = Popen([REDSHELL_NMAP, '-oA', nmap_log_file]+args, bufsize=1)
            sys.stdout.write("[+] Nmap starting [%s]\n" % p.pid)
        else:
            # for now we asume that nmap is in sudeoers passwordless ;p
            # user ALL = (root) NOPASSWD: /usr/local/bin/nmap
            # TODO: use pexpect
            p = Popen([REDSHELL_SUDO, REDSHELL_NMAP, '-oA', nmap_log_file+' ']+args, bufsize=1, shell=False)
            sys.stdout.write("[+] (sudo) Nmap starting [%s]\n" % p.pid)
    except:
        sys.stdout.write("[!] Error: "+sys.exc_info()[0])

    return SHELL_STATUS_RUN