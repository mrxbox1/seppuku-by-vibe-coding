# Fixed duplicate of main.py with clearer character names, a Jack Black option,
# cleaned quotes (no stray newlines), and a dynamic title underline for alignment.
import random
import time

QUOTES = [
    "Make cod go vroom",
    "I like cheese",
    "Breathe water, not air",
    "Pull and peel licorice",
    "Smell the taste of the spooky pasta",
]

CHOICES = {
    "1": "Cod (Variant A)",
    "2": "Cod (Variant B)",
    "3": "Cod (Variant C)",
    "4": "Jack Black",
}


def main():
    title = "COD_REV - The Game"
    # Keep the title visually aligned regardless of terminal width by using a
    # minimum width and centering the text.
    width = max(len(title), 50)
    print(title.center(width))
    print("-" * width)
    print()

    print(random.choice(QUOTES))

    print("Welcome to the game! Please choose a character:")
    print("1 - Cod (Variant A)")
    print("2 - Cod (Variant B)")
    print("3 - Cod (Variant C)")
    print("4 - Jack Black")

    # Validate input
    while True:
        choice = input("Enter 1-4: ").strip()
        if choice in CHOICES:
            chosen_char = CHOICES[choice]
            break
        print("Invalid choice. Please enter a number between 1 and 4.")

    print(f"Nice! You picked {chosen_char}! Let's go to the race!")

    # Game loop behavior depends on selected character in a robust way.
    ch_up = chosen_char.upper()
    if ch_up.startswith("COD"):
        for i in range(5):
            print(f"{chosen_char} flopped in circles.")
            time.sleep(1)
        print("GAME OVER")
    elif ch_up == "JACK BLACK":
        print(f"{chosen_char} rocks the stage and stuns the competition.")
        print("YOU WON")
        print(f"{chosen_char} leveled up to LV 9000.")
    else:
        print(f"{chosen_char} does something unexpected...")


if __name__ == "__main__":
    main()
