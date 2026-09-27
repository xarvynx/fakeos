#!/usr/bin/env python3
"""
FakeOS - A terminal-based fake operating system
Enhanced with nerd fonts, animations, and colors
"""

# imports
import time
import random
import shlex
import sys
import os
import config

from utils import rm_, calc
from games import guessr
from tools import clear, neofetch, hacknasa, time_show, todo
from ZFS import FakeFS, FakeFSError
from math_tool import math_cli

# Import visuals from shared module
from visuals import (C, S, ICON, colorize, gradient, spinner_animation, 
                     progress_bar, clear_screen, print_box, boot_animation)

fs = FakeFS()


# ═══════════════════════════════════════════════════════════════
# COMMAND IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════

def su():
    """Switch to root user with password."""
    if config.current_user == "root":
        print(f'{S.WARN}{ICON.WARNING} Already Root!{C.R}')
        return
    
    print(f'{S.INFO}{ICON.LOCK} Authentication required{C.R}')
    pwd = input(f'{S.CMD}Password: {C.R}')
    
    # Simulate authentication
    spinner_animation('Verifying credentials...', 0.8)
    
    if pwd == config.password:
        config.current_user = "root"
        print(f'{S.OK}{ICON.CHECK} Authentication successful! {S.ROOT}Root access granted{C.R}')
    else:
        print(f'{S.ERR}{ICON.CROSS} Incorrect password{C.R}')


def whoami():
    """Display current user."""
    user_icon = ICON.ROOT if config.current_user == 'root' else ICON.USER
    user_color = S.ROOT if config.current_user == 'root' else S.USER
    print(f'{user_color}{user_icon} {config.current_user}{C.R}')


def help_cmd():
    """Display help with styled boxes."""
    print()
    
    # Filesystem commands
    fs_cmds = [
        f'{S.CMD}pwd{C.R}           {S.DIM}Print working directory{C.R}',
        f'{S.CMD}ls [path]{C.R}     {S.DIM}List directory contents{C.R}',
        f'{S.CMD}cd [path]{C.R}     {S.DIM}Change directory{C.R}',
        f'{S.CMD}mkdir <name>{C.R}  {S.DIM}Create directory{C.R}',
        f'{S.CMD}touch <name> [c]{C.R}{S.DIM}Create file{C.R}',
        f'{S.CMD}write <n> <c>{C.R}  {S.DIM}Write file (overwrite){C.R}',
        f'{S.CMD}cat <name>{C.R}     {S.DIM}Read file{C.R}',
        f'{S.CMD}rm [-r] <name>{C.R} {S.DIM}Remove file or directory (-r recursive){C.R}',
        f'{S.CMD}rmdir <name>{C.R}  {S.DIM}Remove empty directory{C.R}',
        f'{S.CMD}tree [path]{C.R}   {S.DIM}Show directory tree (default: cwd){C.R}',
        f'{S.CMD}echo <text>{C.R}   {S.DIM}Print text{C.R}',
        f'{S.CMD}echo > file{C.R}   {S.DIM}Write to file{C.R}',
        f'{S.CMD}echo >> file{C.R}  {S.DIM}Append to file{C.R}',
    ]
    print_box('FILESYSTEM', fs_cmds, 65, ICON.DIR)
    print()
    
    # System commands
    sys_cmds = [
        f'{S.CMD}whoami{C.R}        {S.DIM}Show current user{C.R}',
        f'{S.CMD}su{C.R}            {S.DIM}Switch to root (password){C.R}',
        f'{S.CMD}clear{C.R}         {S.DIM}Clear screen{C.R}',
        f'{S.CMD}time{C.R}          {S.DIM}Show current time{C.R}',
        f'{S.CMD}neofetch{C.R}      {S.DIM}System information{C.R}',
        f'{S.CMD}help{C.R}          {S.DIM}Show this help{C.R}',
        f'{S.CMD}exit{C.R}          {S.DIM}Shutdown FakeOS{C.R}',
    ]
    print_box('SYSTEM', sys_cmds, 65, ICON.SETTINGS)
    print()
    
    # Apps
    app_cmds = [
        f'{S.CMD}calc{C.R}          {S.DIM}Basic calculator{C.R}',
        f'{S.CMD}guessr{C.R}        {S.DIM}Number guessing game{C.R}',
        f'{S.CMD}todo{C.R}          {S.DIM}To-Do list (persistent){C.R}',
        f'{S.CMD}math / solve{C.R}  {S.DIM}AI math solver{C.R}',
    ]
    print_box('APPLICATIONS', app_cmds, 65, ICON.TERMINAL)
    print()
    
    # Fun commands
    fun_cmds = [
        f'{S.CMD}rm -rf /{C.R}      {S.WARN}Fake system wipe (root){C.R}',
        f'{S.CMD}hacknasa{C.R}      {S.WARN}Fake NASA hack{C.R}',
    ]
    print_box('FUN (Harmless)', fun_cmds, 65, ICON.HACK)
    print()


# ═══════════════════════════════════════════════════════════════
# COMMAND REGISTRY
# ═══════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════

def parse_echo_args(arg: str):
    """Parse echo arguments with support for > and >> redirection."""
    if ">>" in arg:
        parts = arg.split(">>", 1)
        return parts[0].rstrip(), parts[1].lstrip(), True
    elif ">" in arg:
        parts = arg.split(">", 1)
        return parts[0].rstrip(), parts[1].lstrip(), False
    return arg, None, False


# ═══════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════

def get_prompt() -> str:
    """Generate the prompt string with colors and icons."""
    user_icon = ICON.ROOT if config.current_user == 'root' else ICON.USER
    user_color = S.ROOT if config.current_user == 'root' else S.USER
    host_color = S.HOST
    path_color = S.PATH
    prompt_color = S.ROOT if config.current_user == 'root' else S.PROMPT
    
    cwd = fs.pwd()
    # Shorten home directory
    if cwd.startswith('/home/guest'):
        cwd = '~' + cwd[11:]
    
    return (f'{user_color}{user_icon} {config.current_user}{C.R}'
            f'{S.DIM}@{C.R}{host_color}fakeos{C.R}'
            f'{S.DIM}:{C.R}{path_color}{cwd}{C.R}'
            f'{prompt_color} {ICON.PROMPT} {C.R}')


def main():
    """Main event loop."""
    while True:
        try:
            user_input = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print(f'\n{S.INFO}{ICON.SHUTDOWN} Shutting Down FakeOS...{C.R}')
            spinner_animation('Saving state', 0.5)
            print(f'{S.OK}{ICON.CHECK} Goodbye!{C.R}')
            break

        if not user_input.strip():
            continue

        if user_input.strip().lower() == "exit":
            print(f'{S.INFO}{ICON.SHUTDOWN} Shutting Down FakeOS...{C.R}')
            spinner_animation('Saving state', 0.5)
            print(f'{S.OK}{ICON.CHECK} Goodbye!{C.R}')
            break

        # split into command word + the rest (path/text), so args actually work
        parts = user_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "pwd":
            print(f'{ICON.DIR} {S.PATH}{fs.pwd()}{C.R}')

        elif cmd == "ls":
            try:
                result = fs.ls(arg)
                if result:
                    # Colorize output
                    items = result.split('  ')
                    colored = []
                    for item in items:
                        # Check if it's a directory (would need fs check)
                        colored.append(f'{S.PATH}{ICON.FILE} {item}{C.R}')
                    print('  '.join(colored))
                else:
                    print(f'{S.DIM}(empty){C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "cd":
            try:
                fs.cd(arg)
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "mkdir":
            try:
                fs.mkdir(arg)
                print(f'{S.OK}{ICON.CHECK} {ICON.ADD} Created directory: {S.PATH}{arg}{C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "touch":
            try:
                parts = shlex.split(arg) if arg else []
                if not parts:
                    print(f'{S.ERR}{ICON.CROSS} touch: missing file operand{C.R}')
                else:
                    name = parts[0]
                    content = parts[1] if len(parts) > 1 else ""
                    fs.touch(name, content)
                    print(f'{S.OK}{ICON.CHECK} {ICON.ADD} Created file: {S.PATH}{name}{C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "write":
            try:
                parts = shlex.split(arg) if arg else []
                if len(parts) < 2:
                    print(f'{S.ERR}{ICON.CROSS} write: usage: write <filename> <content>{C.R}')
                else:
                    name = parts[0]
                    content = " ".join(parts[1:])
                    fs.write(name, content)
                    print(f'{S.OK}{ICON.CHECK} {ICON.EDIT} Written to: {S.PATH}{name}{C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "rm":
            # Parse flags
            parts = arg.split() if arg else []
            recursive = False
            target = ""
            
            for part in parts:
                if part in ("-r", "-rf", "-fr"):
                    recursive = True
                elif part == "-rf/":
                    # Special case: "rm -rf /" triggers the fake system wipe
                    rm_()
                    recursive = None  # marker that we handled it
                    break
                elif not part.startswith("-"):
                    target = part
            
            if recursive is None:
                continue  # fake wipe was triggered
            
            if not target:
                print(f'{S.ERR}{ICON.CROSS} rm: missing operand{C.R}')
            else:
                try:
                    fs.rm(target, recursive=recursive)
                    print(f'{S.OK}{ICON.CHECK} {ICON.DELETE} Removed: {S.PATH}{target}{C.R}')
                except FakeFSError as e:
                    print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "tree":
            try:
                # Default to current directory if no path given
                path = arg if arg else "."
                print(fs.tree(path))
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "rmdir":
            try:
                if not arg:
                    print(f'{S.ERR}{ICON.CROSS} rmdir: missing operand{C.R}')
                else:
                    fs.rm(arg, recursive=False)
                    print(f'{S.OK}{ICON.CHECK} {ICON.DELETE} Removed directory: {S.PATH}{arg}{C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "cat":
            try:
                content = fs.cat(arg)
                print(f'{S.DIM}─── {S.PATH}{arg} {S.DIM}───{C.R}')
                print(content)
                print(f'{S.DIM}────────────────────{C.R}')
            except FakeFSError as e:
                print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd == "echo":
            text, redirect, append = parse_echo_args(arg)
            if redirect is None:
                print(text)
            else:
                try:
                    fs.echo(text, redirect=redirect, append=append)
                    action = 'Appended to' if append else 'Written to'
                    print(f'{S.OK}{ICON.CHECK} {action}: {S.PATH}{redirect}{C.R}')
                except FakeFSError as e:
                    print(f'{S.ERR}{ICON.CROSS} {e}{C.R}')

        elif cmd in commands:
            commands[cmd]()

        else:
            print(f'{S.ERR}{ICON.CROSS} \'{cmd}\' is not a valid command{C.R}')
            print(f'{S.DIM}Type {S.CMD}help{S.DIM} for available commands{C.R}')


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    boot_animation(config.current_user)
    main()