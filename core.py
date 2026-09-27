#imports
import time
import random
import shlex
import config

from utils import rm_, calc
from games import guessr
from tools import clear, neofetch, hacknasa, time_show, todo
from ZFS import FakeFS, FakeFSError
from math_tool import math_cli

fs = FakeFS()


def startup():
    print("Turning on FakeOS...")
    time.sleep(0.2)
    print("Initializing Kernel...")
    print(f"Welcome {config.current_user}")
    print("")


startup()


def su():
    if config.current_user == "root":
        print("Already Root!")
    else:
        pwd = input("Password: ")
        if pwd == config.password:
            config.current_user = "root"
            print("You're now Root")
        else:
            print("Incorrect password")


# whoami
def whoami():
    print(f"{config.current_user}")


# help
def help_cmd():
    print('''
Available Commands Are:

help
exit
ls
pwd
cd
cat
mkdir
touch
write
rm
tree
echo
whoami
su
calc
guessr
time
neofetch
todo
clear
math / solve

rm -rf /
hacknasa
''')


# old ls() / cd() placeholders removed - the real filesystem (fs) handles
# these now, since they need arguments (a path) and the old dict-lookup
# style couldn't pass any.

commands = {
    "clear": clear,
    "help": help_cmd,
    "neofetch": neofetch,
    "hacknasa": hacknasa,
    "whoami": whoami,
    "su": su,
    "time": time_show,
    "guessr": guessr,
    "calc": calc,
    "todo": todo,
    "math": math_cli,
    "solve": math_cli,
    "rm -rf /": rm_,
}


def parse_echo_args(arg: str):
    """Parse echo arguments with support for > and >> redirection.
    Returns (text, redirect_target, append_flag) or (text, None, False) if no redirection.
    """
    # Find the last > or >> that isn't quoted
    # Simple approach: look for >> first, then >
    if ">>" in arg:
        parts = arg.split(">>", 1)
        return parts[0].rstrip(), parts[1].lstrip(), True
    elif ">" in arg:
        parts = arg.split(">", 1)
        return parts[0].rstrip(), parts[1].lstrip(), False
    return arg, None, False


def main():
    while True:
        user_input = input(f"{config.current_user}@fakeos> ")

        if not user_input.strip():
            continue

        if user_input.strip().lower() == "exit":
            print("Shutting Down FakeOS")
            break

        # split into command word + the rest (path/text), so args actually work
        parts = user_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "pwd":
            print(fs.pwd())

        elif cmd == "ls":
            try:
                result = fs.ls(arg)
                if result:
                    print(result)
                else:
                    print("(empty)")
            except FakeFSError as e:
                print(e)

        elif cmd == "cd":
            try:
                fs.cd(arg)
            except FakeFSError as e:
                print(e)

        elif cmd == "mkdir":
            try:
                fs.mkdir(arg)
            except FakeFSError as e:
                print(e)

        elif cmd == "touch":
            try:
                # touch filename [content]
                parts = shlex.split(arg) if arg else []
                if not parts:
                    print("touch: missing file operand")
                else:
                    name = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                    fs.touch(name, content)
            except FakeFSError as e:
                print(e)

        elif cmd == "write":
            try:
                # write filename content
                parts = shlex.split(arg) if arg else []
                if len(parts) < 2:
                    print("write: usage: write <filename> <content>")
                else:
                    name = parts[0]
                    content = " ".join(parts[1:])
                    fs.write(name, content)
            except FakeFSError as e:
                print(e)

        elif cmd == "rm":
            # Special case: "rm -rf /" triggers the fake system wipe
            if arg.strip() == "-rf /":
                rm_()
            else:
                try:
                    fs.rm(arg)
                except FakeFSError as e:
                    print(e)

        elif cmd == "tree":
            try:
                print(fs.tree(arg))
            except FakeFSError as e:
                print(e)

        elif cmd == "cat":
            try:
                print(fs.cat(arg))
            except FakeFSError as e:
                print(e)

        elif cmd == "echo":
            text, redirect, append = parse_echo_args(arg)
            if redirect is None:
                print(text)
            else:
                try:
                    fs.echo(text, redirect=redirect, append=append)
                except FakeFSError as e:
                    print(e)

        elif cmd in commands:
            commands[cmd]()

        else:
            print(f"'{cmd}' is not a valid command. Enter 'help' for a list of available commands!")


main()
