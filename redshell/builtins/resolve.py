#! /usr/bin/env python
import sys
import dns.resolver,dns.zone,dns.reversename
from redshell.config import *

# TODO: use custom resolver
# TODO: version.bind chaos

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
    sys.stdout.write("[+] Resolving "+h+" \n")
    for ip in dns.resolver.query(h, 'A'):
        try:
            hostname = dns.reversename.from_address(str(ip))
            sys.stdout.write("[*] IP: "+str(ip)+" \t-> "+hostname+"\n")
        except:
            sys.stdout.write("[*] IP: "+str(ip)+"\n")

    # Get MX records, resolve to IP and PTR
    try:
        for mx in dns.resolver.query(h, 'MX'):
            try:
                ip = dns.reversename.to_address(str(mx))
                hostname = dns.reversename.from_address(ip)
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
                ip = dns.reversename.to_address(str(ns))
                hostname = dns.reversename.from_address(ip)
                sys.stdout.write("[ ] NS: "+str(ns)+" \t-> "+ip+" \t-> "+hostname+"\n")
            except:
                sys.stdout.write("[ ] NS: "+str(ns)+" \t-> "+ip+"\n")
                    
    except:
        pass

    # Check for AAAA records
    try:    
        for aaaa in dns.resolver.query(h, 'AAAA'):
            sys.stdout.write("[ ] AAAA: "+str(aaaa)+"\n")        
    except:
        pass
 
    # Check for TXT  records
    try:    
        for txt in dns.resolver.query(h, 'TXT'):
            sys.stdout.write("[ ] TXT: "+str(txt)+"\n")        
    except:
        pass
 
    return SHELL_STATUS_RUN


