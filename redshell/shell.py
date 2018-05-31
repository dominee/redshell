import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from redshell.constants import *
from redshell.builtins import *
from redshell.prompt import *
from redshell.config import *

# Hash map to store built-in function name and reference as key and value
built_in_cmds = {}


def tokenize(string):
    return shlex.split(string)


def preprocess(tokens):
    processed_token = []
    for token in tokens:
        # Convert $-prefixed token to value of an environment variable
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token


def handler_kill(signum, frame):
    raise OSError("Killed!")


def execute(cmd_tokens):
    if cmd_tokens:

        # Extract command name and arguments from tokens
        cmd_name = cmd_tokens[0]
        cmd_args = cmd_tokens[1:]
        # Log command to history
        with open(REDSHELL_HISTORY, 'a') as history_file:
            history_file.write(' '.join(cmd_tokens) + os.linesep)

        # Show list of available command and their short usage
        if cmd_name == 'help' or cmd_name == 'usage':
            for cmd_name in built_in_cmds:
                try:
                    built_in_cmds[cmd_name](['usage'])
                except:
                    pass
            return SHELL_STATUS_RUN

        # If the command is a built-in command,
        # invoke its function with arguments
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)

        # Wait for a kill signal
        signal.signal(signal.SIGINT, handler_kill)
        # Spawn a child process
        if platform.system() != "Windows":
            # Unix support
            p = subprocess.Popen(cmd_tokens)
            # Parent process read data from child process
            # and wait for child process to exit
            p.communicate()
        else:
            # Windows support
            command = ""
            for i in cmd_tokens:
                command = command + " " + i
            os.system(command)
    # Return status indicating to wait for next command in shell_loop
    return SHELL_STATUS_RUN


def ignore_signals():
    # Ignore Ctrl-Z stop signal
    if platform.system() != "Windows":
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    # Ignore Ctrl-C interrupt signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()

        # Ignore Ctrl-Z and Ctrl-C signals
        ignore_signals()

        try:
            # Read command input
            cmd = sys.stdin.readline()
            # Tokenize the command input
            cmd_tokens = tokenize(cmd)
            # Preprocess special tokens
            # (e.g. convert $<env> into environment value)
            cmd_tokens = preprocess(cmd_tokens)
            # Execute the command and retrieve new status
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            print(err)


# Register a built-in function to built-in command hash map
def register_command(name, func):
    built_in_cmds[name] = func


# Register all built-in commands here
def init():
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("export", export)
    register_command("getenv", getenv)
    register_command("history", history)
    register_command("burp", burp)
    register_command("nmap", nmap)
    register_command("owasp", owasp)
    register_command("resolve", resolve)
    register_command("project", project)


def main():
    # Init shell before starting the main loop
    init()
    shell_loop()

if __name__ == "__main__":
    main()
