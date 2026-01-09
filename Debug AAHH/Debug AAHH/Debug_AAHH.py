import random

def play_game_fixed():
    secret_number = random.randint(1,100)
    guess_count = 0
    
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    user_guess = None # Initialize to a value that won't match the secret number
    
    while user_guess != secret_number:
        try:
            user_guess = int(input("Enter your guess: "))
            guess_count += 1
            
            if user_guess < secret_number:
                print("Too low! Try again.")
            elif user_guess > secret_number:
                print("Too high! Try again.")
        except ValueError:
            # Handle non-integer input gracefully
            print("Invalid input. Please enter a number.")
            
    print(f"Congratulations! You guessed it in {guess_count} guesses.")

play_game_fixed()
