import random

answer = random.randint(1, 1000)
run = True
big = 1000
small = 1
attempts = 10

while run:
    if attempts <= 0:
        print("Game Over!")
        print("="*20)
        exit()
    try:
        print("="*20)
        guess = int(input(f"Guess number between {small} and {big} ({attempts} attempts left)\nYour guess: "))
    except:
        print("Try again")
        continue

    if guess == answer:
        print("You win!")
        print("="*20)
        exit()
    elif guess < answer:
        if guess > small:
            small = guess
        attempts -= 1
        print("More!")
    else:
        if guess < big:
            big = guess
        attempts -= 1
        print("Less!")