import config
import time

# Calculator:
def calc():
    print("Basic Calculator")
    print("Type 'exit' at any prompt to leave.")

    while True:
        first = input("First Number: ")

        if first.lower() == "exit":
            break

        try:
            num1 = float(first)
        except ValueError:
            print("Please enter a valid number.")
            continue

        second = input("Second Number: ")
        if second.lower() == "exit":
            break

        try:
            num2 = float(second)
        except ValueError:
            print("Please enter a valid number.")
            continue

        op = input("Operator (+ - * /): ")
        if op.lower() == "exit":
            break

        if op == "+":
            print("Answer:", num1 + num2)

        elif op == "-":
            print("Answer:", num1 - num2)

        elif op == "*":
            print("Answer:", num1 * num2)

        elif op == "/":
            if num2 == 0:
                print("You can't divide by zero!")
            else:
                print("Answer:", num1 / num2)

        else:
            print("Invalid operator!")


def rm_():
    if config.current_user == "guest":
        print("You need to be root to perform this function!")
        return

    if config.current_user == "root":
        print('''
Recursively Removing /
Deleting /etc/
Deleting /boot/
Deleting /bin/
Deleting /dev/
Unmounting Partitions...
               ''')

        time.sleep(2)
        print("System Halted. Unknown Error Occurred!")
        time.sleep(2)
        print("Recovering.....")
        time.sleep(5)