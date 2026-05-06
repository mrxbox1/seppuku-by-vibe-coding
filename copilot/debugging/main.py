# This is a cleaned-up duplicate of main.py with input validation and improved structure.
import random
import time

QUOTES = [
    "\nMake cod go vroom\n",
    "\nI like cheese\n",
    "\nBreathe water, not air",
    "\nPull and peel licorice\n\n",
    "Smell the taste of the spooky pasta",
]

CHOICES = {
    "1": "COD",
    "2": "COD",
    "3": "COD",
    "4": "JOHN WICK",
}


def main():
    print("COD_REV - The Game")
    print("-" * 25)

    print(random.choice(QUOTES))

    print("Welcome to the game! Please choose a character:")
    print("1 - Cod (variant A)")
    print("2 - Cod (variant B)")
    print("3 - Cod (variant C)")
    print("4 - John Wick")

    # Validate input
    while True:
        choice = input("Enter 1-4: ").strip()
        if choice in CHOICES:
            chosen_char = CHOICES[choice]
            break
        print("Invalid choice. Please enter a number between 1 and 4.")

    print(f"Nice! You picked {chosen_char}! Let's go to the race!")

    # Game loop: use clear conditionals and avoid always-true mistakes
    if chosen_char == "COD":
        # Give COD a short sequence rather than an infinite loop
        for i in range(5):
            print(f"{chosen_char} flopped in circles.")
            time.sleep(1)
        print("GAME OVER")
    elif chosen_char == "JOHN WICK":
        print(f"{chosen_char} killed contestants #2, #3, and #4 using a gun.")
        print("YOU WON")
        print(f"{chosen_char} leveled up to LV 999.")
        print(f"{chosen_char} approaches you with the intent to decapitate someone.")


if __name__ == "__main__":
    main()
