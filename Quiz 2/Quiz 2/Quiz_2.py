
number_to_guess = 3

max_tries = 5

tries = 0

print("Let's play a guessing game!")
print("Guess the number between 1 and 10.")
print("You have 5 tries to guess the correct number.")


while tries < max_tries:
    guess = input("Enter your guess: ")
    tries += 1

    if guess.isdigit():
        guess = int(guess)
    else:
        print("Please enter a number.")
        continue

    if guess == number_to_guess:
        print("You win! You guessed it right!")
        break
    else:
        print("Nope, try again.")

if tries == max_tries:
    print("Game over! You didn't guess it this time."))