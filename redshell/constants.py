import os
from termcolor import colored

SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

DEFAULT_REDSHELL_DIR = '~'+os.sep+'.redshell'
DEFAULT_REDSHELL_HISTORY = '~'+os.sep+'.redshell_history'
DEFAULT_REDSHELL_REPORTS = '~'+os.sep+'Documents'+os.sep+'redshell_reports/'

DEFAULT_REDSHELL_NMAP = '/usr/local/bin/nmap'
DEFAULT_REDSHELL_SUDO = '/usr/bin/sudo'
DEFAULT_REDSHELL_DIG = '/usr/bin/dig'

DEFAULT_REDSHELL_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0"
DEFAULT_REDSHELL_PROXY = '127.0.0.1:8080'
DEFAULT_REDSHELL_COLLABORATOR = 'r.batata.sk'
DEFAULT_HOST = 'localhost'

# Colored line markers
line_start = lambda x: colored('[','white')+colored(x,'red')+colored('] ','white')
LS = line_start(' ')
PLUS = line_start('+')
MINUS = line_start('-')
STAR = line_start('*')
EX = line_start('!')
