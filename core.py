#imports
import time
import random
import config

from utils import rm_, calc
from games import guessr
from tools import clear, neofetch, hacknasa, time_show, todo
from ZFS import FakeFS, FakeFSError

fs = FakeFS()


def startup():
    print("Turning on FakeOS...")
    time.sleep(0.2)
    print("Initialsing Kernel...")
    print(f"Welcome {config.current_user}")
    print("")


startup()


def su():
    if config.current_user == "root":
        print("Already Root!")
    else:
        config.current_user = "root"
        print("You're now Root")


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
echo
whoami
su
calc
guessr
time
neofetch
todo

rm -rf /
hacknasa
''')


def hacknasa():
    time.sleep(1)
    print("Initialsing Nmap, msf console, ")
    time.sleep(1)
    print("Launching attack!")
    time.sleep(0.5)
    print("Gaining access...")
    time.sleep(0.5)
    print("Err. Occured! No Internet Detected")


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
    "rm -rf /": rm_,
}


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
                print(fs.ls(arg))
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

        elif cmd == "cat":
            try:
                print(fs.cat(arg))
            except FakeFSError as e:
                print(e)


        elif cmd == "echo":
            if ">>" in arg:
                text, target = arg.split(">>", 1)
                try:
                    fs.echo(text.strip(), redirect=target.strip(), append=True)
                except FakeFSError as e:
                    print(e)
            elif ">" in arg:
                text, target = arg.split(">", 1)
                try:
                    fs.echo(text.strip(), redirect=target.strip())
                except FakeFSError as e:
                    print(e)
            else:
                print(fs.echo(arg))

        elif user_input.strip().lower() in commands:
            commands[user_input.strip().lower()]()

        else:
            print(f"'{user_input}' is not a valid command enter 'help' for a list of available commands!")


main()
