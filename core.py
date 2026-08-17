#imports
import time
import random

import config
from utils import rm_, calc
from games import guessr
from tools import clear, neofetch, hacknasa, time_show, todo

current_user = "guest"

def startup():
    print("Turning on FakeOS...")
    time.sleep(0.2)
    print("Initialsing Kernel...")
    print(f"Welcome {current_user}")
    print("")
startup()

def su():
    if config.current_user == "root":
        print("Already Root!")

    else:
        config.current_user = "root"
        print("You're now Root")

#whoami
def whoami():
    print(f"{current_user}")

#help
def help_cmd():
    print('''
Available Commands Are:

help
exit
ls
cd
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


#ls
def ls():
    print('''
B2 Bomber BluePrints
/
mnt
etc
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

#cd
def cd():
    print("Changed Directory")


commands = {"ls": ls, "clear": clear, "cd": cd, "help": help_cmd, "neofetch": neofetch, "hacknasa": hacknasa, "whoami": whoami, "su": su, "time": time_show,
            "guessr": guessr, "calc": calc, "todo": todo, "rm -rf /": rm_
 }


def main():
    while True:
        user_input = input(f"{config.current_user}@fakeos> ").lower()
        if user_input == "exit":
            print("Shutting Down FakeOS")
            break
        
        if not user_input:
            continue
        
        if user_input in commands:
            command_function = commands[user_input]
            command_function()

        else:
            print(f"'{user_input}' is not a valid command enter 'help' for a list of available commands!")
main()
