import random

def showdice(n):
    if n == 1:
        print("[-----]")
        print("[     ]")
        print("[  *  ]")
        print("[     ]")
        print("[-----]")
    elif n == 2:
        print("[-----]")
        print("[*    ]")
        print("[     ]")
        print("[    *]")
        print("[-----]")
    elif n == 3:
        print("[-----]")
        print("[*    ]")
        print("[  *  ]")
        print("[    *]")
        print("[-----]")
    elif n == 4:
        print("[-----]")
        print("[*   *]")
        print("[     ]")
        print("[*   *]")
        print("[-----]")
    elif n == 5:
        print("[-----]")
        print("[*   *]")
        print("[  *  ]")
        print("[*   *]")
        print("[-----]")
    elif n == 6:
        print("[-----]")
        print("[*   *]")
        print("[*   *]")
        print("[*   *]")
        print("[-----]")

guess = 1
r = 02
count = 0
while r != guess:
    guess = int(input("Guess the dice roll (1-6): "))
    r = random.randint(1, 6)
    showdice(r)
count = count += 1

print(f"Correct! It took you {count} tries.")


