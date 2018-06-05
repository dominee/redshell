#! /usr/bin/env python

import itertools
import re
from redshell.config import *
from termcolor import colored
from redshell.constants import DEFAULT_HOST

# Generate hostnames to populate fuzz_list
host_1 = colored("h1."+REDSHELL_COLLABORATOR,"red")
host_2 = colored("h2."+REDSHELL_COLLABORATOR,"yellow")
host_3 = colored("h3."+REDSHELL_COLLABORATOR,"white")

# Ports and schemes to apply
schemes = ["http", "https"]
ports = ["80", "443"]
# List of parser bypasses from Orange
fuzz_list = [
    "{scheme}://{h1} &@{h2}# @{h3}/",
    "{scheme}://{h1}:{port1}:{port2}/",
    "{scheme}://{h1}#@{h2}/",
    "{scheme}://foo@{h1}:{port1}@{h2}/",
    "{scheme}://foo@{h1} @{h2}/",
    "{scheme}://{h1}\\t{h2}/",
    "{scheme}://{h1}%09{h2}/",
    "{scheme}://{h1}%2509{h2}/",
    "{scheme}://0/",
    "{scheme}://{h1}/"
]

# taken from https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address/106223#106223
ValidIpAddressRegex = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
ValidHostnameRegex = r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";

def urlfuzz_help():
    sys.stdout.write("""
[urlfuzz]
Usage : urlfuzz [whitelisted-host]

Generate URLs for fuzzing url-parsers. Without parameter 'localhost' is used.

Examples: 
urlfuzz
urlfuzz example.com
""")
    return SHELL_STATUS_RUN

def urlfuzz_usage():
    sys.stdout.write(colored("urlfuzz","white")+" [host]\n")
    return SHELL_STATUS_RUN


def urlfuzz(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return urlfuzz_help()
        if args[0] == 'usage':
            return urlfuzz_usage()

        # Check for host params
        if re.match(ValidHostnameRegex,args[0]) or re.match(ValidIpAddressRegex,args[0]):
            host=colored(args[0],'green')
        # In case the first argument is an invalid host or IP, exit
        else:
            urlfuzz_usage()
            return SHELL_STATUS_RUN
    else:
        # Use 'localhost' as default vale
        host = colored(DEFAULT_HOST,'green')
        sys.stdout.write(STAR+"Host not specified. Using default: "+host+"\n")

    # Generate host combinations
    fuzzed = set()
    for i in itertools.product(schemes, [host,host_1], [host,host_2], [host,host_3], ports, ports):
        if i[1] == i[2] or i[4] == i[5]:
            continue
        for u in fuzz_list:
            fuzzed.add(u.format(scheme=i[0], h1=i[1], h2=i[2], h3=i[3], port1=i[4], port2=i[5]))

    for f in fuzzed:
        if host in f:
            sys.stdout.write(f+"\n")
    
    return SHELL_STATUS_RUN