import config
import time

#Calculator:
def calc():
    print("Basic Calculator")
    print("Type 'exit' to leave.")

    while True:
        first = input("First Number: ")

        if first.lower() == "exit":
            break

        try:
            num1 = float(first)
            num2 = float(input("Second Number: "))
            op = input("Operator (+ - * /): ")

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

        except ValueError:
                print("Please enter valid numbers.")



def rm_():
    if config.current_user == "guest":
        print("You need to be root to Perform this function!")
    
    elif config.current_user == "root":
        print('''
Recursively Removing /
Deleting /etc/
Deleting /boot/
Deleting /bin/
Deleting /boot/
Deleting /dev/
Unmounting Partitons...
              ''')

        time.sleep(2)
        print("System Halted. Unknown Error Occured!")
        time.sleep(2)
        print("Recovering.....")
        time.sleep(5)

























