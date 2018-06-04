#! /usr/bin/env python
from redshell.config import *
import requests
import httplib
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ProxyError
from termcolor import colored

# yes, we ignroe SSL warning on purpose ;p
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False

# set proxy to config values
proxies = {'http': 'http://'+REDSHELL_PROXY,
           'https': 'https://'+REDSHELL_PROXY}
session.proxies = proxies
# Set request headers 
headers = {"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1",
           "Accept-Language": "en-US,en;q=0.5", "User-Agent": REDSHELL_UA, "Connection": "close"}


def owasp_help():
    sys.stdout.write("""
[owasp]
Usage : owasp <url>

Generate HTTP requests via PROXY to automate some OTG-* sections.

Examples: 
owasp https://example.com
""")
    return SHELL_STATUS_RUN

def owasp_usage():
    sys.stdout.write(colored("owasp","white")+" <url>\n")
    return SHELL_STATUS_RUN

def owasp(args):
    
    if len(args) > 0:
         # Do we need to display usage or help?
        if args[0] == 'help':
            return owasp_help()
        if args[0] == 'usage':
            return owasp_usage()
        if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})?(?:/[\w&%?#-]{1,300})?',args[0]):
            host = args[0]
        else:
            owasp_usage()
            return SHELL_STATUS_RUN
    else:
        owasp_usage()

    try:
        # test requests to check if proxy is available
        response = session.get(host + '/', headers=headers, verify=False)
    except ProxyError:
        print MINUS+"Proxy is not available, disabling."
        session.proxies = None
    

    # OTG-INFO-* stuff
    paths = ['/','/robots.txt','/crossdomain.xml','/clientaccesspolicy.xml']
    for path in paths:
        response = session.get(host + path, headers=headers, verify=False)
        print(LS+"%i %s" % (colored(response.status_code,'white'),path))

    # Request errors
    # 400 Bad Request - unknown method (WTF)
    response = session.request('WTF',host + '/', headers=headers, verify=False)
    print(LS+"Bad Request (WTF) [400] : %i"  % colored(response.status_code,'white'))

    # 405 Method Not Allowed
    response = session.request('MKCOL',host + '/', headers=headers, verify=False)
    print(LS+"Method Not Allowed (MKCOL) [405] : %i"  % colored(response.status_code,'white'))

    # 414 URI Too Long
    paramsGet = {"very_long_param": "A"*10097}
    response = session.get(host + "/", params=paramsGet, headers=headers, verify=False)
    print(LS+"URI Too Long [414] : %i"  % colored(response.status_code,'white'))

    # 413 Payload Too Large
    rawBody = "A"*1024*1024*5
    response = session.post(host + "/", data=rawBody, headers=headers,verify=False)
    print(LS+"Payload Too Large [413] : %i"  % colored(response.status_code,'white'))

    # 417 Expectation Failed
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": REDSHELL_UA, "Connection": "close","Expect":"666-evil"}, verify=False)
    print(LS+"Expectation Failed [417] : %i"  % colored(response.status_code,'white'))


    # 431 Request Header Fields Too Large
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": 'A'*10097, "Connection": "close"}, verify=False)
    print(LS+"Request Header Fields Too Large [431] : %i"  % colored(response.status_code,'white'))

    # 505 HTTP Version Not Supported
    vsn =  httplib.HTTPConnection._http_vsn
    vsn_str = httplib.HTTPConnection._http_vsn_str
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    response = session.get(host + '/', headers=headers, verify=False)
    print(LS+"HTTP Version Not Supported [505] : %i"  % colored(response.status_code,'white'))
    httplib.HTTPConnection._http_vsn = vsn
    httplib.HTTPConnection._http_vsn_str = vsn_str

    # 101 Switching Protocols
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1","Accept-Language": "en-US,en;q=0.5", "User-Agent": REDSHELL_UA, "Connection": "Upgrade", "Upgrade":"websocket"}, verify=False)
    print(LS+"101 Switching Protocols (websocket) [101] : %i"  % colored(response.status_code,'white'))

    return SHELL_STATUS_RUN

