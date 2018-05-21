#! /usr/bin/env python
from redshell.config import *
import requests
import httplib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ProxyError

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False

# TODO: This should be placed in config
proxies = {'http': 'http://127.0.0.1:8080',
           'https': 'https://127.0.0.1:8080'}
session.proxies = proxies
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0"
headers = {"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1",
           "Accept-Language": "en-US,en;q=0.5", "User-Agent": user_agent, "Connection": "close"}


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
    sys.stdout.write("owasp <url>\n")
    return SHELL_STATUS_RUN

def owasp(args):
    
    if len(args) > 0:
         # Do we need to display usage or help?
        if args[0] == 'help':
            return owasp_help()
        if args[0] == 'usage':
            return owasp_usage()
        # TODO: check if it is a valid url
        host = args[0]
    else:
        owasp_usage()

    try:
        # test requests to check if proxy is available
        response = session.get(host + '/', headers=headers, verify=False)
    except ProxyError:
        print '[-] Proxy is not available, disabling.'
        session.proxies = None
    

    # OTG-INFO-* stuff
    paths = ['/','/robots.txt','/crossdomain.xml','/clientaccesspolicy.xml']
    for path in paths:
        response = session.get(host + path, headers=headers, verify=False)
        print("[ ] %i %s" % (response.status_code,path))

    # Request errors
    # 400 Bad Request - unknown method (WTF)
    response = session.request('WTF',host + '/', headers=headers, verify=False)
    print("[ ] Bad Request (WTF) [400] : %i"  % response.status_code)

    # 405 Method Not Allowed
    response = session.request('MKCOL',host + '/', headers=headers, verify=False)
    print("[ ] Method Not Allowed (MKCOL) [405] : %i"  % response.status_code)

    # 414 URI Too Long
    paramsGet = {"very_long_param": "A"*10097}
    response = session.get(host + "/", params=paramsGet, headers=headers, verify=False)
    print("[ ] URI Too Long [414] : %i"  % response.status_code)

    # 413 Payload Too Large
    rawBody = "A"*1024*1024*3
    response = session.post(host + "/", data=rawBody, headers=headers,verify=False)
    print("[ ] Payload Too Large [413] : %i"  % response.status_code)

    # 417 Expectation Failed
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": user_agent, "Connection": "close","Expect":"666-evil"}, verify=False)
    print("[ ] Expectation Failed [417] : %i"  % response.status_code)


    # 431 Request Header Fields Too Large
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": 'A'*10097, "Connection": "close"}, verify=False)
    print("[ ] Request Header Fields Too Large [431] : %i"  % response.status_code)

    # 505 HTTP Version Not Supported
    vsn =  httplib.HTTPConnection._http_vsn
    vsn_str = httplib.HTTPConnection._http_vsn_str
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    response = session.get(host + '/', headers=headers, verify=False)
    print("[ ] HTTP Version Not Supported [505] : %i"  % response.status_code)
    httplib.HTTPConnection._http_vsn = vsn
    httplib.HTTPConnection._http_vsn_str = vsn_str

    # 101 Switching Protocols
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1","Accept-Language": "en-US,en;q=0.5", "User-Agent": user_agent, "Connection": "Upgrade", "Upgrade":"websocket"}, verify=False)
    print("[ ] 101 Switching Protocols (websocket) [101] : %i"  % response.status_code)

    return SHELL_STATUS_RUN

