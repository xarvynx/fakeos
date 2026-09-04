import random 

def guessr(): 
    secret = random.randint(1, 100) 
    print("Guessr* -") 
    attempts = 0 
    
    while True: 
        attempts += 1 
        guess = input("Enter a Guess or 'exit': ") 
        
        if guess == "exit": 
            break 
        else:
            try:
                guess = int(guess) 
            
                if guess == secret: 
                    print(f"You won!, Attempts : {attempts}") 
                    break  
                
                elif guess > secret: 
                    print("too high") 
                
                elif guess < secret: 
                    print("too low") 
    
            except ValueError:
                print("Numbers Only")



            

