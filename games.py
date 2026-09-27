# games.py
import random
import time

from visuals import (C, S, ICON, colorize, gradient, spinner_animation, 
                     progress_bar, clear_screen, print_box)


def guessr():
    """Enhanced number guessing game with colors and animations."""
    clear_screen()
    
    print_box('GUESSR', [
        f'{S.CMD}Guess a number between 1-100{C.R}',
        f'{S.CMD}Type "exit" to quit{C.R}',
        f'{S.CMD}Type "hint" for a clue{C.R}',
    ], 50, ICON.GAME)
    print()
    
    secret = random.randint(1, 100)
    attempts = 0
    hints_used = 0
    
    while True:
        try:
            guess = input(f'{S.CMD}Guess #{attempts + 1}: {C.R}').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not guess:
            continue
            
        if guess in ("exit", "quit", "q"):
            print(f'{S.WARN}{ICON.WARNING} Game quit. The number was {S.CMD}{secret}{S.WARN}.{C.R}')
            break
            
        if guess in ("hint", "h", "?"):
            hints_used += 1
            if hints_used == 1:
                print(f'{S.INFO}{ICON.INFO} Hint: The number is {"even" if secret % 2 == 0 else "odd"}{C.R}')
            elif hints_used == 2:
                print(f'{S.INFO}{ICON.INFO} Hint: The number is {"greater" if secret > 50 else "less than or equal to"} 50{C.R}')
            elif hints_used == 3:
                range_size = 10
                low = max(1, secret - range_size // 2)
                high = min(100, low + range_size)
                print(f'{S.INFO}{ICON.INFO} Hint: The number is between {low} and {high}{C.R}')
            else:
                print(f'{S.WARN}{ICON.WARNING} No more hints available!{C.R}')
            continue
            
        try:
            guess_num = int(guess)
            if guess_num < 1 or guess_num > 100:
                print(f'{S.ERR}{ICON.CROSS} Please enter a number between 1 and 100!{C.R}')
                continue
        except ValueError:
            print(f'{S.ERR}{ICON.CROSS} Numbers only!{C.R}')
            continue
            
        attempts += 1
        
        if guess_num == secret:
            print(f'{S.OK}{ICON.CHECK} {ICON.STAR} You won! {ICON.STAR}{C.R}')
            print(f'{S.INFO}Attempts: {S.CMD}{attempts}{C.R}')
            if hints_used:
                print(f'{S.DIM}Hints used: {hints_used}{C.R}')
            
            # Performance rating
            if attempts <= 5:
                rating = f'{S.OK}{ICON.HEART} Legendary!{C.R}'
            elif attempts <= 10:
                rating = f'{S.OK}{ICON.STAR} Great job!{C.R}'
            elif attempts <= 20:
                rating = f'{S.INFO}{ICON.INFO} Good!{C.R}'
            else:
                rating = f'{S.WARN}{ICON.WARNING} Keep practicing!{C.R}'
            print(f'{rating}')
            break
            
        elif guess_num > secret:
            diff = guess_num - secret
            if diff <= 5:
                print(f'{S.WARN}{ICON.ARROW} Too high! (very close){C.R}')
            elif diff <= 15:
                print(f'{S.WARN}{ICON.ARROW} Too high!{C.R}')
            else:
                print(f'{S.ERR}{ICON.ARROW2} Way too high!{C.R}')
                
        elif guess_num < secret:
            diff = secret - guess_num
            if diff <= 5:
                print(f'{S.INFO}{ICON.ARROW} Too low! (very close){C.R}')
            elif diff <= 15:
                print(f'{S.INFO}{ICON.ARROW} Too low!{C.R}')
            else:
                print(f'{S.ERR}{ICON.ARROW2} Way too low!{C.R}')


def snake():
    """Placeholder for snake game."""
    print(f'{S.INFO}{ICON.GAME} Snake game coming soon!{C.R}')
    print(f'{S.DIM}Use arrow keys to control the snake{C.R}')


def tetris():
    """Placeholder for tetris game."""
    print(f'{S.INFO}{ICON.GAME} Tetris game coming soon!{C.R}')
    print(f'{S.DIM}Rotate and drop tetrominoes{C.R}')