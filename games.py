import random
def guessr():
    secret = random.randint(1, 100)
    print("Guessr* -")
    attempts = 0
    while True:
        guess_1 = int(input("Enter Your Guess or 'exit' : "))
        if guess_1 == exit:
            break

        else:
            continue

        attempts += 1
        try:
            guess = int(guess_1)
            if guess == secret:
                print("You've Won 1 Million Robux YAYYYY and a free virus")
                print("Tries Took", attempts)
                break
            elif guess < secret:
                print("Too Lowwww")

            elif guess > secret:
                print("Too Highhh")
            else:
                print("Try Again!")
        
        except ValueError:
            print("Enter an Number (Real Number)")

