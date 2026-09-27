# utils.py
import config
import time
import random

from visuals import (C, S, ICON, colorize, gradient, spinner_animation, 
                     progress_bar, clear_screen, print_box)


# Calculator:
def calc():
    """Enhanced calculator with colors and better UX."""
    clear_screen()
    print_box('CALCULATOR', [
        f'{S.CMD}Enter numbers and operator{C.R}',
        f'{S.CMD}Operators: + - * / % ** //{C.R}',
        f'{S.CMD}Type "exit" at any prompt to quit{C.R}',
        f'{S.CMD}Type "clear" to clear screen{C.R}',
        f'{S.CMD}Type "help" for more info{C.R}',
    ], 55, ICON.CALC)
    print()
    
    # Show some examples
    examples = [
        ('2 + 3', '5'),
        ('10 - 4', '6'),
        ('6 * 7', '42'),
        ('20 / 4', '5'),
        ('2 ** 10', '1024'),
        ('17 % 5', '2'),
        ('10 // 3', '3'),
    ]
    print(f'{S.DIM}Examples:{C.R}')
    for expr, result in examples:
        print(f'  {S.CMD}{expr:<10}{C.R} = {S.OK}{result}{C.R}')
    print()
    
    while True:
        try:
            first = input(f'{S.CMD}First Number: {C.R}').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not first:
            continue
        if first.lower() in ("exit", "quit", "q"):
            print(f'{S.OK}{ICON.CHECK} Exiting Calculator...{C.R}')
            break
        if first.lower() == "clear":
            clear_screen()
            print_box('CALCULATOR', [
                f'{S.CMD}Enter numbers and operator{C.R}',
                f'{S.CMD}Operators: + - * / % ** //{C.R}',
                f'{S.CMD}Type "exit" at any prompt to quit{C.R}',
            ], 55, ICON.CALC)
            print()
            continue
        if first.lower() == "help":
            print_box('HELP', [
                f'{S.CMD}+{C.R}  Addition',
                f'{S.CMD}-{C.R}  Subtraction',
                f'{S.CMD}*{C.R}  Multiplication',
                f'{S.CMD}/{C.R}  Division',
                f'{S.CMD}%{C.R}  Modulo (remainder)',
                f'{S.CMD}**{C.R} Power',
                f'{S.CMD}//{C.R} Floor division',
            ], 35, ICON.INFO)
            continue
            
        try:
            num1 = float(first)
        except ValueError:
            print(f'{S.ERR}{ICON.CROSS} Please enter a valid number.{C.R}')
            continue

        try:
            second = input(f'{S.CMD}Second Number: {C.R}').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not second:
            continue
        if second.lower() in ("exit", "quit", "q"):
            print(f'{S.OK}{ICON.CHECK} Exiting Calculator...{C.R}')
            break
            
        try:
            num2 = float(second)
        except ValueError:
            print(f'{S.ERR}{ICON.CROSS} Please enter a valid number.{C.R}')
            continue

        try:
            op = input(f'{S.CMD}Operator (+ - * / % ** //): {C.R}').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not op:
            continue
        if op.lower() in ("exit", "quit", "q"):
            print(f'{S.OK}{ICON.CHECK} Exiting Calculator...{C.R}')
            break
            
        # Perform calculation
        spinner_animation('Calculating...', 0.3)
        
        try:
            if op == "+":
                result = num1 + num2
                symbol = "+"
            elif op == "-":
                result = num1 - num2
                symbol = "−"
            elif op == "*":
                result = num1 * num2
                symbol = "×"
            elif op == "/":
                if num2 == 0:
                    print(f'{S.ERR}{ICON.CROSS} Cannot divide by zero!{C.R}')
                    continue
                result = num1 / num2
                symbol = "÷"
            elif op == "%":
                result = num1 % num2
                symbol = "%"
            elif op == "**":
                result = num1 ** num2
                symbol = "^"
            elif op == "//":
                if num2 == 0:
                    print(f'{S.ERR}{ICON.CROSS} Cannot divide by zero!{C.R}')
                    continue
                result = num1 // num2
                symbol = "//"
            else:
                print(f'{S.ERR}{ICON.CROSS} Invalid operator! Use: + - * / % ** //{C.R}')
                continue
                
            # Format result nicely
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.10g}"
                
            print(f'{S.OK}{ICON.CHECK} {S.CMD}{num1:g} {symbol} {num2:g} = {result_str}{C.R}')
            print(f'{S.DIM}──────────────────────────────{C.R}')
            
        except OverflowError:
            print(f'{S.ERR}{ICON.CROSS} Result too large!{C.R}')
        except Exception as e:
            print(f'{S.ERR}{ICON.CROSS} Error: {e}{C.R}')


def rm_():
    """Enhanced fake system wipe with animations."""
    if config.current_user == "guest":
        print(f'{S.ERR}{ICON.CROSS} {ICON.LOCK} You need to be root to perform this function!{C.R}')
        return
    
    if config.current_user == "root":
        print(f'{S.WARN}{ICON.WARNING} {S.B}WARNING: This will simulate a system wipe!{C.R}')
        confirm = input(f'{S.ERR}Type "YES" to confirm: {C.R}').strip()
        if confirm != "YES":
            print(f'{S.OK}{ICON.CHECK} Operation cancelled.{C.R}')
            return
        
        print()
        print(f'{S.ERR}{ICON.BOLT} INITIATING RECURSIVE REMOVAL OF / {C.R}')
        print()
        
        # Animated deletion
        dirs = [
            '/etc/', '/boot/', '/bin/', '/sbin/', '/lib/', '/usr/',
            '/var/', '/tmp/', '/home/', '/root/', '/dev/', '/proc/',
            '/sys/', '/run/', '/opt/', '/srv/', '/mnt/', '/media/',
        ]
        
        for d in dirs:
            # Random chance to show "deleting" vs "unmounting"
            if random.random() < 0.8:
                print(f'{S.ERR}{ICON.DELETE} Deleting {S.PATH}{d}{C.R}')
            else:
                print(f'{S.WARN}{ICON.WARNING} Unmounting {S.PATH}{d}{C.R}')
            time.sleep(random.uniform(0.05, 0.15))
        
        print()
        progress_bar('Wiping filesystem metadata', 20, 0.03)
        time.sleep(0.5)
        
        print(f'{S.ERR}{ICON.CROSS} {S.B}SYSTEM HALTED. UNKNOWN ERROR OCCURRED!{C.R}')
        time.sleep(2)
        
        print(f'{S.INFO}{ICON.LOADING} Attempting recovery...{C.R}')
        progress_bar('Recovering boot sector', 15, 0.05)
        progress_bar('Restoring kernel', 15, 0.05)
        progress_bar('Remounting partitions', 15, 0.05)
        
        time.sleep(1)
        print(f'{S.OK}{ICON.CHECK} {S.B}RECOVERY COMPLETE. SYSTEM OPERATIONAL.{C.R}')
        print(f'{S.DIM}    All fake data preserved. No actual harm done.{C.R}')