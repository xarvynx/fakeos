# tools.py
import time
import os


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


todo_list = []
def todo():
    print("This is a CLI Based To-Do App!")
    print("Functions : (add, remove, list, help, clear(clears screen) or exit)")
    while True:
        todo_func = input("todo> ").lower()
        if todo_func == "exit":
            break
        elif todo_func == "clear":
            clear()
        
        elif todo_func == "add":
            task = input("Enter a Task : ").strip()
            if task:
                todo_list.append(task)
                print(f"Added Task '{task}'")
            else:
                print("Task Cannot be empty!")

        elif todo_func == "list":
            if not todo_list:
                print("Your To-Do List is currently empty!")
            else:
                print("Your Tasks are: ")
                for index, task in enumerate(todo_list, start=1):
                    print(f"{index}. {task}")

        elif todo_func == "remove":
            try:
                # 1. Get the input as a string first so we can check if it's empty
                user_input = input("Enter what to remove (1,2,3..) or enter to cancel: ").strip()
                
                # 2. Check if the user just pressed Enter to cancel
                if not user_input:
                    print("Cancelled. Nothing removed.")
                    
                else:
                    # 3. Convert to integer now that we know it's not empty
                    to_remove = int(user_input)
                    
                    # 4. Check if the number actually exists in your list
                    if 1 <= to_remove <= len(todo_list):
                        # 5. Subtract 1 to match Python's 0-based index
                        removed_task = todo_list.pop(to_remove - 1)
                        print(f"Removed task: '{removed_task}'")
                    else:
                        print("Error: Invalid task number!")
            except ValueError:
                print("Error Numbers only!")







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
