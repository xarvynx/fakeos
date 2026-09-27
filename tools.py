# tools.py
import time
import os
import json

TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakeos_todo.json")


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


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
    print("This is a CLI Based To-Do App!")
    print("Functions: (add, remove, list, help, clear(clears screen) or exit)")
    while True:
        todo_func = input("todo> ").lower()
        if todo_func == "exit":
            break
        elif todo_func == "clear":
            clear()

        elif todo_func == "help":
            print("Commands: add, remove, list, clear, exit")

        elif todo_func == "add":
            task = input("Enter a Task: ").strip()
            if task:
                todo_list.append(task)
                _save_todos(todo_list)
                print(f"Added Task '{task}'")
            else:
                print("Task cannot be empty!")

        elif todo_func == "list":
            if not todo_list:
                print("Your To-Do List is currently empty!")
            else:
                print("Your Tasks are:")
                for index, task in enumerate(todo_list, start=1):
                    print(f"{index}. {task}")

        elif todo_func == "remove":
            try:
                user_input = input("Enter what to remove (1,2,3..) or press Enter to cancel: ").strip()

                if not user_input:
                    print("Cancelled. Nothing removed.")

                else:
                    to_remove = int(user_input)

                    if 1 <= to_remove <= len(todo_list):
                        removed_task = todo_list.pop(to_remove - 1)
                        _save_todos(todo_list)
                        print(f"Removed task: '{removed_task}'")
                    else:
                        print("Error: Invalid task number!")
            except ValueError:
                print("Error: Numbers only!")


def neofetch():
    print('''
System Specifications:
    4gb ram
    Intel Celeron J3060
    500 GB HDD
    ''')


def hacknasa():
    time.sleep(1)
    print("Initializing Nmap, msf console... ")
    time.sleep(1)
    print("Launching attack!")
    time.sleep(0.5)
    print("Gaining access...")
    time.sleep(0.5)
    print("Err. Occurred! No Internet Detected")


def time_show():
    print(time.ctime())