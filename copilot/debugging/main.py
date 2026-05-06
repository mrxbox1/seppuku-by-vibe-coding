# This file was written by a human being.
# Please don't touch it.

import random as rand
import time

print("COD_REV - The Game")
print("-"*25)

print(rand.choice(["\nMake cod go vroom\n", "\nI like cheese\n", "\nBreathe water, not air", "\nPull and peel licorice\n\n", "Smell the taste of the spooky pasta"]))

print("Welcome to the game! Ples choose a character:")
print("1 - Cod")
print("2 - Cod")
print("3 - Cod")
print("4 - John Wick")

chosen_char = input()
if chosen_char == "1":
    chosen_char = "COD"
if chosen_char == "2":
    chosen_char = "COD"
if chosen_char == "3":
    chosen_char = "COD"
if chosen_char == "4":
    chosen_char = "JOHN WICK"

print("Nice! You picked", chosen_char, "! Let's go to the race!")

while True:
    print("-"*25)
    if chosen_char == "COD" or "COD" or "COD":
        print(chosen_char, "flopped in circles.")
    if chosen_char == "JOHN WICK":
        print(chosen_char, "killed contestants #2, #3, and #4 using a gun.")
        break
    time.sleep(1)

print("YOU WON")
print("JOHN WICK leveled up to LV 999.")
print("JOHN WICK approaches you with the intent to decapitate someone.")
