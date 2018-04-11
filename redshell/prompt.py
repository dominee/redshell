from termcolor import colored
import os
import sys
import socket
import getpass

TRIANGLE = u'\ue0b0'
SEPARATOR = u'\ue0b1'

prompt_start = lambda x: colored(" "+x+" ",'white','on_red')+colored(TRIANGLE,'red','on_white')
prompt_start_for_two = lambda x: colored(" "+x+" ",'white','on_red')+colored(SEPARATOR,'white','on_red')
prompt_middle = lambda x: colored(" "+x+" ",'red','on_white')+colored(SEPARATOR,'red','on_white')
prompt_middle_last = lambda x: colored(" "+x+" ",'red','on_white')+colored(TRIANGLE,'white','on_red')
prompt_end = lambda x: colored(" "+x+" ",'white','on_red')+colored(TRIANGLE,'red')

def prompt(*argv):
    prompt_string = prompt_end('$')
    if len(argv)==2:
        prompt_string = prompt_start_for_two(argv[0])+prompt_end(argv[1])
    if len(argv)==3:
        prompt_string = prompt_start(argv[0])+prompt_middle_last(argv[1])+prompt_end(argv[2])
    if len(argv)>=4:
        prompt_string = prompt_start(argv[0])
        for arg in argv[1:-2]:
            prompt_string += prompt_middle(arg)
        prompt_string += prompt_middle_last(argv[-2])    
        prompt_string += prompt_end(argv[-1])

    return prompt_string+' '

# Display a command prompt as `[<user>@<hostname> <dir>]$ `
def display_cmd_prompt():
    # Get user and hostname
    user = getpass.getuser()
    hostname = socket.gethostname()

    # Get base directory (last part of the curent working directory path)
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)

    # Use ~ instead if a user is at his/her home directory
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # Print out to console

    sys.stdout.write(prompt(user, hostname, base_dir,'$'))
    sys.stdout.flush()
