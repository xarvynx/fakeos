# tools.py
import time
import os
import json
import socket
import platform

from visuals import (C, S, ICON, colorize, gradient, spinner_animation, 
                     progress_bar, clear_screen, print_box)

TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakeos_todo.json")


def _load_todos():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_todos(todos):
    try:
        with open(TODO_FILE, "w") as f:
            json.dump(todos, f, indent=2)
    except OSError:
        pass


todo_list = _load_todos()


def todo():
    """Enhanced To-Do app with colors and icons."""
    clear_screen()
    print_box('TO-DO LIST', [
        f'{S.CMD}add <task>{C.R}      {S.DIM}Add a new task{C.R}',
        f'{S.CMD}list{C.R}            {S.DIM}List all tasks{C.R}',
        f'{S.CMD}remove <num>{C.R}     {S.DIM}Remove task by number{C.R}',
        f'{S.CMD}clear{C.R}           {S.DIM}Clear screen{C.R}',
        f'{S.CMD}help{C.R}            {S.DIM}Show this help{C.R}',
        f'{S.CMD}exit{C.R}            {S.DIM}Return to FakeOS{C.R}',
    ], 55, ICON.TODO)
    print()
    
    while True:
        try:
            user_input = input(f'{S.CMD}todo{S.DIM}> {C.R}').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not user_input:
            continue
            
        parts = user_input.split(maxsplit=1)
        todo_func = parts[0].lower()
        todo_arg = parts[1] if len(parts) > 1 else ""
            
        if todo_func == "exit":
            print(f'{S.OK}{ICON.CHECK} Exiting To-Do...{C.R}')
            break
        elif todo_func == "clear":
            clear_screen()
            print_box('TO-DO LIST', [
                f'{S.CMD}add <task>{C.R}      {S.DIM}Add a new task{C.R}',
                f'{S.CMD}list{C.R}            {S.DIM}List all tasks{C.R}',
                f'{S.CMD}remove <num>{C.R}     {S.DIM}Remove task by number{C.R}',
                f'{S.CMD}clear{C.R}           {S.DIM}Clear screen{C.R}',
                f'{S.CMD}help{C.R}            {S.DIM}Show this help{C.R}',
                f'{S.CMD}exit{C.R}            {S.DIM}Return to FakeOS{C.R}',
            ], 55, ICON.TODO)
            print()
        elif todo_func == "help":
            print_box('COMMANDS', [
                f'{S.CMD}add <task>{C.R}      {S.DIM}Add a new task{C.R}',
                f'{S.CMD}list{C.R}            {S.DIM}List all tasks{C.R}',
                f'{S.CMD}remove <num>{C.R}     {S.DIM}Remove task by number{C.R}',
                f'{S.CMD}clear{C.R}           {S.DIM}Clear screen{C.R}',
                f'{S.CMD}help{C.R}            {S.DIM}Show this help{C.R}',
                f'{S.CMD}exit{C.R}            {S.DIM}Return to FakeOS{C.R}',
            ], 55, ICON.INFO)
        elif todo_func == "add":
            task = todo_arg.strip()
            if not task:
                task = input(f'{S.CMD}Task: {C.R}').strip()
            if task:
                todo_list.append(task)
                _save_todos(todo_list)
                print(f'{S.OK}{ICON.CHECK} {ICON.ADD} Added: {S.PATH}{task}{C.R}')
            else:
                print(f'{S.ERR}{ICON.CROSS} Task cannot be empty!{C.R}')
        elif todo_func == "list":
            if not todo_list:
                print(f'{S.DIM}{ICON.INFO} Your To-Do List is empty{C.R}')
            else:
                print(f'{S.INFO}{ICON.TODO} Your Tasks:{C.R}')
                for index, task in enumerate(todo_list, start=1):
                    status = f'{S.OK}{ICON.CHECK}{C.R}' if index <= 3 else f'{S.DIM}○{C.R}'
                    print(f'  {S.CMD}{index:2d}.{C.R} {status} {task}')
        elif todo_func == "remove":
            try:
                user_input = input(f'{S.CMD}Remove (1,2,3..) or Enter to cancel: {C.R}').strip()
                if not user_input:
                    print(f'{S.WARN}{ICON.WARNING} Cancelled{C.R}')
                else:
                    to_remove = int(user_input)
                    if 1 <= to_remove <= len(todo_list):
                        removed_task = todo_list.pop(to_remove - 1)
                        _save_todos(todo_list)
                        print(f'{S.OK}{ICON.CHECK} {ICON.REMOVE} Removed: {S.PATH}{removed_task}{C.R}')
                    else:
                        print(f'{S.ERR}{ICON.CROSS} Invalid task number!{C.R}')
            except ValueError:
                print(f'{S.ERR}{ICON.CROSS} Numbers only!{C.R}')
        else:
            print(f'{S.ERR}{ICON.CROSS} Unknown command: {todo_func}{C.R}')


def neofetch():
    """System information display."""
    clear_screen()
    
    # Get system info
    try:
        hostname = socket.gethostname()
    except:
        hostname = 'fakeos'
    
    try:
        os_name = platform.system()
        os_version = platform.release()
    except:
        os_name = 'FakeOS'
        os_version = '2.1.0'
    
    try:
        python_version = platform.python_version()
    except:
        python_version = '3.x'
    
    # FakeOS specific info
    user = os.getenv('USER', 'guest')
    shell = 'fakeos-shell'
    uptime = '0 days, 0 hours, 0 mins'
    
    # Simple banner
    print(f'{S.TITLE}{ICON.OS} System Information{C.R}')
    print(f'{S.DIM}──────────────────────────────────────{C.R}')
    print()
    
    # System info
    try:
        term_size = os.get_terminal_size()
        term_info = f'{term_size.columns}x{term_size.lines}'
    except OSError:
        term_info = 'N/A (non-TTY)'
    
    info_lines = [
        (f'{ICON.USER} User', f'{user}'),
        (f'{ICON.OS} OS', f'{os_name} {os_version}'),
        (f'{ICON.TERMINAL} Shell', f'{shell}'),
        (f'{ICON.KEY} Python', f'{python_version}'),
        (f'{ICON.TIME} Uptime', f'{uptime}'),
        (f'{ICON.DIR} Home', f'/home/{user}'),
        (f'{ICON.GEAR} Kernel', f'FakeOS Kernel 2.1.0'),
        (f'{ICON.CALC} Tasks', f'{len(todo_list)} in todo'),
        (f'{ICON.HACK} Terminal', term_info),
    ]
    
    for label, val in info_lines:
        print(f'  {S.INFO}{label:<15}{C.R} {S.PATH}{val}{C.R}')
    
    print()


def hacknasa():
    """Enhanced fake NASA hack with animations."""
    print(f'{S.INFO}{ICON.HACK} Initializing Nmap, msfconsole...{C.R}')
    spinner_animation('Scanning targets...', 1.0)
    spinner_animation('Launching exploit...', 1.0)
    spinner_animation('Gaining access...', 1.0)
    time.sleep(0.5)
    print(f'{S.ERR}{ICON.CROSS} ERROR: No internet connection detected{C.R}')
    print(f'{S.DIM}    Connection timeout - attack aborted{C.R}')


def time_show():
    """Enhanced time display."""
    current_time = time.ctime()
    print(f'{ICON.TIME} {S.CMD}{time.strftime("%A, %B %d, %Y")}{C.R}')
    print(f'{ICON.TIME} {S.CMD}{time.strftime("%H:%M:%S %Z")}{C.R}')
    print(f'{S.DIM}    Unix timestamp: {int(time.time())}{C.R}')


def clear():
    """Clear screen."""
    clear_screen()