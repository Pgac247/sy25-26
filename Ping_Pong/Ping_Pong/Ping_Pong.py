import random

player1_score = 0
player2_score = 0

print("Press Enter to hit the ball. First to 10 wins!")
while player1_score < 10 and player2_score < 10:
    input("Player 1, press Enter to hit the ball: ")
    roll = random.randint(1, 6)
    if roll == 1:
        player2_score += 1
        print("Miss! Player 2 scores.")
    elif roll == 6:
        player1_score += 1
        print("Nice hit! Player 1 scores.")
    else:
        print("Ball returned.")
    print(f"Scores => Player 1: {player1_score} | Player 2: {player2_score}")

print("Game over!")
if player1_score >= 10:
    print("Player 1 wins!")
else:
    print("Player 2 wins!")