#! /usr/bin/env python
import socket
import sys
import dns.resolver,dns.zone
from redshell.config import *

def resolve_help():
    sys.stdout.write("""
[resolve]
Usage : resolve <domain>

Resolve a domain name recursively

Examples: 
resolve github.com
""")
    return SHELL_STATUS_RUN

def resolve_usage():
    sys.stdout.write("resolve <domain>\n")
    return SHELL_STATUS_RUN

def resolve(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return resolve_help()
        if args[0] == 'usage':
            return resolve_usage()
        h = args[0]
    else:
        resolve_usage()

    # Check for A and CNAME
    # TODO: Check AAAA
    sys.stdout.write("[+] Resolving "+h+" \n")
    host,aliases,ips = socket.gethostbyname_ex(h)
    if host and host != h: sys.stdout.write("[ ] %s is an alias for %s\n" % (h,host))
    if aliases:
        sys.stdout.write("[ ] Alias: ")
        for alias in aliases: 
            sys.stdout.write(alias+" ")
        sys.stdout.write("\n")
    if ips:
        for ip in ips: 
            try:
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
                sys.stdout.write("[ ] IP: "+ip+" \t-> "+hostname+"\n")
            except:
                sys.stdout.write("[ ] IP: "+ip+"\n")

    # Get MX records, resolve to IP and PTR
    try:
        for mx in dns.resolver.query(h, 'MX'):
            try:
                ip = socket.gethostbyname(str(mx))
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
                sys.stdout.write("[ ] MX: "+str(mx)+" \t-> "+ip+" \t-> "+hostname+"\n")
            except:
                sys.stdout.write("[ ] MX: "+str(mx)+" \t-> "+ip+"\n")
    except:
        pass

    # Get NS records, resolve to IP and PTR
    try:
        for ns in dns.resolver.query(h, 'NS'):
            try:
                # Try to make a AXFR zone transfer
                z = dns.zone.from_xfr(dns.query.xfr(ns, h))
                sys.stdout.write("[!] AXFR:\n")
                names = z.nodes.keys()
                names.sort()
                # If AXFR is possible, print the result
                for n in names:
                    sys.stdout.write(z[n].to_text(n))
                sys.stdout.write("\n")
            except:
                pass
            # If AXFR is not possible, just resolve NS records
            try:
                ip = socket.gethostbyname(str(ns))
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
                sys.stdout.write("[ ] NS: "+str(ns)+" \t-> "+ip+" \t-> "+hostname+"\n")
            except:
                sys.stdout.write("[ ] NS: "+str(ns)+" \t-> "+ip+"\n")
                    
    except:
        pass

    # Check for TXT  records
    try:    
        for txt in dns.resolver.query(h, 'TXT'):
            sys.stdout.write("[ ] TXT: "+str(txt)+"\n")        
    except:
        pass
 
    sys.stdout.write("\n")
    return SHELL_STATUS_RUN


