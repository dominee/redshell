# Redshell - A shell wrapper for (lazy) web pentesters written in Python

Because shell dotfiles are awesome, but sometimes you need something more.

Run with: `python -m redshell.shell`

#  The goal

The goal is to automate all the boring stuff and provide consistent project structure in the team.
The main focus is for web (and mobile) pentests.

* use docker for external tools 
* autoupdate git projects for the tools
* keep the your toolset in one place
* make a wrapper for the tools to automatically store console output and logs ine the designated directories and using the same name convention

```
~/.redshell(.conf)

~/redshell
 |-tools (ext tools)
 |-lists (wordlists)
 |-log/ (log/sslscan/2017/11/12/testssl_1130-domain.log) 
 |-outputs (output/sslscan/2017/11/12/testssl_1130-domain.log) 
```
* autostart the latest version of the burpsuite jar
* create a new folder structure for a new project and populate it with preconfigured skeleton files

```
~/Documents/reports/
 |-2017/11/12/Cutomer-Project/ 
                      |-screenshots
                      |-report
                      |-documentation
                      |-PoC
                      |-burp
                      |-tmp
                      |-log -> ~/redshell/log/
                      |-outputs -> ~/redshell/outputs/
                      |-OWASP-OTG-v4.todo
                      |-notes.txt
```

* start listeners local or remote and notify you on a request
* generate payloads for defined listeners
* copy predefined polyglots for fuzzing to clipboard
* run all info gathering and enumeration tools in one command
* update env variables with scope, host and cookies from burp and browser
* use the nice command prompt from powerlines