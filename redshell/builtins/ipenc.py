#! /usr/bin/env python
import sys
import re
from redshell.config import *
from termcolor import colored

encodings_dots = ("%02x", "%04o", "%d")
encodings = ("0x%x", "0%o", "%d")

def ipenc_help():
    sys.stdout.write("""
[ipenc]
Usage : ipenc <ip>

Show alternate IP forms for the specified IP.

Examples: 
ipenc 127.0.01
""")
    return SHELL_STATUS_RUN

def ipenc_usage():
    sys.stdout.write(colored("ipenc","white")+" <ip>\n")
    return SHELL_STATUS_RUN

def join_dots(s, length=4):
    ret = ""
    for i in range(length - 1):
        ret += s + "."
    ret += s
    return ret

def ip_fuzz_dots(ip, encodings):
    ip_dec = tuple(map(int, ip.split('.')))

    for e in encodings:
        format_string = join_dots(e)
        print(format_string % ip_dec)

def ip_fuzz(ip, encodings):
    ip_dec = tuple(map(int, ip.split('.')))
    ip_dec = ip_dec[0] * 256**3 + ip_dec[1] * 256**2 + ip_dec[2] * 256 + ip_dec[3]

    for e in encodings:
        print(e % ip_dec)

def ipenc(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return ipenc_help()
        if args[0] == 'usage':
            return ipenc_usage()

        # Check for IP argument
        if re.match(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',args[0]):
            ip=args[0]
        else:
            ipenc_usage()
            return SHELL_STATUS_RUN
    else:
        ipenc_usage()
        return SHELL_STATUS_RUN

    # Calculate IP variants and display them
    sys.stdout.write(STAR+colored(ip,"white")+"\n")
    ip_fuzz_dots(ip, encodings_dots)
    ip_fuzz(ip, encodings)
    return SHELL_STATUS_RUN