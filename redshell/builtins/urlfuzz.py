#! /usr/bin/env python

import itertools
import re
from redshell.config import *
from termcolor import colored

allowed = ["localhost"]
schemes = ["http", "https"]
first = "first.p.batata.sk"
second = "second.p.batata.sk"
third = "third.p.batata.sk"

hostlist = [colored(first,'green'), colored(second,'red'), colored(third,'yellow')] + allowed
ports = ["80", "443"]


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
Usage : urlfuzz <ip>

Generate URLs for fuzzing url-parsers.

Examples: 
urlfuzz 
""")
    return SHELL_STATUS_RUN

def urlfuzz_usage():
    sys.stdout.write(colored("urlfuzz","white")+" <url1>\n")
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
            host=args[0]
        else:
            urlfuzz_usage()
            return SHELL_STATUS_RUN
    else:
        urlfuzz_usage()
        return SHELL_STATUS_RUN

    fuzzed = set()
    for i in itertools.product(schemes, hostlist, hostlist, hostlist, ports, ports):
        if i[1] == i[2] or i[4] == i[5]:
            continue
        for u in fuzz_list:
            fuzzed.add(u.format(scheme=i[0], h1=i[1], h2=i[2], h3=i[3], port1=i[4], port2=i[5]))

    for f in fuzzed:
        print(f)
    
    return SHELL_STATUS_RUN