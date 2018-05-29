#! /usr/bin/env python
import sys
import dns.resolver,dns.zone,dns.reversename
from redshell.config import *

# TODO: use custom resolver
# TODO: version.bind chaos

def resolve_help():
    sys.stdout.write("""
[resolve]
Usage : resolve <domain> [nameserver]

Resolve a domain name recursively

Examples: 
resolve github.com
""")
    return SHELL_STATUS_RUN

def resolve_usage():
    sys.stdout.write("resolve <domain> [nameserver]\n")
    return SHELL_STATUS_RUN

def resolve(args):

    if len(args) > 0:
        # Do we need to display usage or help?
        if args[0] == 'help':
            return resolve_help()
        if args[0] == 'usage':
            return resolve_usage()

        # Create our own resolver instance
        my_resolver = dns.resolver.Resolver()
        my_resolver.timeout = 1
        my_resolver.lifetime = 1
        # Assign target domain/host
        h = args[0]
        # If a resolver was specified, use it
        if len(args) == 2:
            my_resolver.nameservers = [args[1]]
            # Check if the resolver is working
            try:
                my_resolver.query('google.com', 'A')[0]
                sys.stdout.write("[+] Nameserver: "+args[1]+"\n")
            except dns.exception.Timeout:
                print 'Resolver timeout.'
                return SHELL_STATUS_RUN
    else:
        resolve_usage()

    # Check for A and CNAME
    sys.stdout.write("[+] Resolving "+h+" \n")
    for ip in my_resolver.query(h, 'A'):
        try:
            hostname = my_resolver.query(dns.reversename.from_address(str(ip)), 'PTR')[0]
            sys.stdout.write("[*] IP: "+str(ip)+" -> "+str(hostname)+"\n")
        except:
            sys.stdout.write("[*] IP: "+str(ip)+"\n")


    # Get MX records, resolve to IP and PTR
    try:
        for mx in my_resolver.query(h, 'MX'):
            try:
                mx_host = str(mx).split(' ')[1]
                ip = my_resolver.query(mx_host, 'A')[0]
                hostname = my_resolver.query(dns.reversename.from_address(str(ip)),'PTR')[0]
                sys.stdout.write("[ ] MX: "+str(mx)+" -> "+str(ip)+" -> "+str(hostname)+"\n")
            except:
                sys.stdout.write("[ ] MX: "+str(mx)+" -> "+str(ip)+"\n")
    except:
        pass
    
    # Get NS records, resolve to IP and PTR
    try:
        for ns in my_resolver.query(h, 'NS'):
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
                ip = my_resolver.query(str(ns), 'A')[0]
                hostname = my_resolver.query(dns.reversename.from_address(str(ip)), 'PTR')[0]
                sys.stdout.write("[ ] NS: "+str(ns)+" -> "+str(ip)+" -> "+str(hostname)+"\n")
            except:
                sys.stdout.write("[ ] NS: "+str(ns)+" -> "+str(ip)+"\n")
                    
    except:
        pass

    # Check for AAAA records
    try:    
        for aaaa in my_resolver.query(h, 'AAAA'):
            sys.stdout.write("[ ] AAAA: "+str(aaaa)+"\n")        
    except:
        pass
 
    # Check for TXT  records
    try:    
        for txt in my_resolver.query(h, 'TXT'):
            sys.stdout.write("[ ] TXT: "+str(txt)+"\n")        
    except:
        pass
 
    return SHELL_STATUS_RUN


