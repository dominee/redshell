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
#clear headers for the beginning
session.headers.clear()
session.headers.update(headers)

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
        print(LS+"%s %s" % (colored(response.status_code,'white'),path))

    # Request errors
    # 400 Bad Request - unknown method (WTF)
    response = session.request('WTF',host + '/', headers=headers, verify=False)
    print(LS+"Bad Request (WTF) [400] : %s"  % colored(response.status_code,'white'))

    # 405 Method Not Allowed
    response = session.request('MKCOL',host + '/', headers=headers, verify=False)
    print(LS+"Method Not Allowed (MKCOL) [405] : %s"  % colored(response.status_code,'white'))

    # 414 URI Too Long
    paramsGet = {"very_long_param": "A"*10097}
    response = session.get(host + "/", params=paramsGet, headers=headers, verify=False)
    print(LS+"URI Too Long [414] : %s"  % colored(response.status_code,'white'))

    # 413 Payload Too Large
    rawBody = "A"*1024*1024*5
    response = session.post(host + "/", data=rawBody, headers=headers,verify=False)
    print(LS+"Payload Too Large [413] : %s"  % colored(response.status_code,'white'))

    # 417 Expectation Failed
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": REDSHELL_UA, "Connection": "close","Expect":"666-evil"}, verify=False)
    print(LS+"Expectation Failed [417] : %s"  % colored(response.status_code,'white'))


    # 431 Request Header Fields Too Large
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Accept-Language": "en-US,en;q=0.5", "User-Agent": 'A'*10097, "Connection": "close"}, verify=False)
    print(LS+"Request Header Fields Too Large [431] : %s"  % colored(response.status_code,'white'))

    # 505 HTTP Version Not Supported
    vsn =  httplib.HTTPConnection._http_vsn
    vsn_str = httplib.HTTPConnection._http_vsn_str
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    response = session.get(host + '/', headers=headers, verify=False)
    print(LS+"HTTP Version Not Supported [505] : %s"  % colored(response.status_code,'white'))
    httplib.HTTPConnection._http_vsn = vsn
    httplib.HTTPConnection._http_vsn_str = vsn_str

    # 101 Switching Protocols
    response = session.get(host + '/', headers={"Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1","Accept-Language": "en-US,en;q=0.5", "User-Agent": REDSHELL_UA, "Connection": "Upgrade", "Upgrade":"websocket"}, verify=False)
    print(LS+"101 Switching Protocols (websocket) [101] : %s"  % colored(response.status_code,'white'))


    # Headers proxy/waf related
    session.headers.clear()
    headers_waf=headers.copy()
    headers_waf_dict={
        "Access-Control-Request-Method": "GET",
        "X-HTTP-Method-Override": "GET",
        "Proxy-Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Forwarded": "for=192.0.2.60;proto=http;by=127.0.0.1",
        "From": "hacker@example.com",
        "Max-Forwards": "1",
        "Referer": "https://127.0.0.1",
        "Via": "1.0 127.0.0.1, 1.1 localhost",
        "X-Forwarded-For": "\"127.0.0.1\", \"192.168.1.1\"",
        "X-Forwarded-Host": "localhost:8080",
        "X-Forwarded-Proto": "https",
        "Proxy-Connection": "keep-alive",
    }

    # Concat the dictionaries
    headers_waf.update(headers_waf_dict)
    response = session.post(host + '/', headers=headers_waf, verify=False)
    print(LS+"Using HTTP headers (proxy/WAF): %s"  % colored(response.status_code,'white'))



# Headers Subset with reasonable headers
    session.headers.clear()
    headers_subset=headers.copy()
    headers_subset_dict={
        "A-IM": "feed",
        "Accept": "text/plain",
        "Accept-Charset": "utf-8",
        "Accept-Datetime": "Thu, 31 May 2007 20:35:00 GMT",
        "Access-Control-Request-Method": "GET",
        "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==",
        "Proxy-Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Content-MD5": "Q2hlY2sgSW50ZWdyaXR5IQ==",
        "Cookie": "$Version=1; Debug=true;",
        "Date": "Tue, 15 Nov 1994 08:12:31 GMT",
        "Expect": "100-continue",
        "Forwarded": "for=192.0.2.60;proto=http;by=127.0.0.1",
        "From": "user@example.com",
        "If-Modified-Since": "Sat, 29 Oct 1994 19:43:31 GMT",
        "Max-Forwards": "5",
        "Origin": "https://kali.citadelo.com",
        "Referer": "https://127.0.0.1",
        "TE": "trailers, deflate",
        "Via": "1.0 127.0.0.1, 1.1 localhost",
        "Warning": "199 Miscellaneous warning",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "X-Forwarded-For": "\"127.0.0.1\", \"192.168.1.1\"",
        "X-Forwarded-Host": "localhost:8080",
        "X-Forwarded-Proto": "https",
        "Front-End-Https": "on",
        "X-HTTP-Method-Override": "GET",
        "X-Att-Deviceid": "GT-P7320/P7320XXLPG",
        "x-wap-profile": "http://wap.samsungmobile.com/uaprof/SGH-I777.xml",
        "Proxy-Connection": "keep-alive",
        "X-UIDH": "supercookie",
        "X-Csrf-Token": "i8XNjC4b8KVok4uw5RftR38Wgp2BFwql",
        "X-Request-ID": "f058ebd6-02f7-4d3f-942e-904344e8cde5"
    }

    # Concat the dictionaries
    headers_subset.update(headers_subset_dict)
    response = session.post(host + '/', headers=headers_subset, verify=False)
    print(LS+"Using HTTP headers (subset): %s"  % colored(response.status_code,'white'))


    # ALL Headers
    session.headers.clear()
    headers_all=headers.copy()
    # List from https://en.wikipedia.org/wiki/List_of_HTTP_header_fields
    headers_big={
        "A-IM": "feed",
        "Accept": "text/plain",
        "Accept-Charset": "utf-8",
        "Accept-Datetime": "Thu, 31 May 2007 20:35:00 GMT",
        "Access-Control-Request-Method": "GET",
        "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==",
        "Proxy-Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Content-MD5": "Q2hlY2sgSW50ZWdyaXR5IQ==",
        "Cookie": "$Version=1; Debug=true;",
        "Date": "Tue, 15 Nov 1994 08:12:31 GMT",
        "Expect": "100-continue",
        "Forwarded": "for=192.0.2.60;proto=http;by=127.0.0.1",
        "From": "user@example.com",
        "If-Modified-Since": "Sat, 29 Oct 1994 19:43:31 GMT",
        "If-Unmodified-Since": "Sat, 29 Oct 1994 19:43:31 GMT",
        "If-Match": "\"737060cd8c284d8af7ad3082f209582d\"",
        "If-None-Match": "\"737060cd8c284d8af7ad3082f209582d\"",
        "If-Range": "\"737060cd8c284d8af7ad3082f209582d\"",
        "Max-Forwards": "5",
        "Origin": "https://kali.citadelo.com",
        "Referer": "https://127.0.0.1",
        "TE": "trailers, deflate",
        "Via": "1.0 127.0.0.1, 1.1 localhost",
        "Warning": "199 Miscellaneous warning",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "X-Forwarded-For": "\"127.0.0.1\", \"192.168.1.1\"",
        "X-Forwarded-Host": "localhost:8080",
        "X-Forwarded-Proto": "https",
        "Front-End-Https": "on",
        "X-HTTP-Method-Override": "GET",
        "X-Att-Deviceid": "GT-P7320/P7320XXLPG",
        "x-wap-profile": "http://wap.samsungmobile.com/uaprof/SGH-I777.xml",
        "Proxy-Connection": "keep-alive",
        "X-UIDH": "supercookie",
        "X-Csrf-Token": "i8XNjC4b8KVok4uw5RftR38Wgp2BFwql",
        "X-Request-ID": "f058ebd6-02f7-4d3f-942e-904344e8cde5"
    }

    # Concat the dictionaries
    headers_all.update(headers_big)
    response = session.post(host + '/', headers=headers_all, verify=False)
    print(LS+"Using ALL HTTP headers : %s"  % colored(response.status_code,'white'))

    # The End
    session.close()
    return SHELL_STATUS_RUN

