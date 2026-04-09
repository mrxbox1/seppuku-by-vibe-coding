# yes, this is inspired by Portal's cake recipe
import random as rand

print("Abnormal cake recipe generator")
print("- "*25)

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
units = ["ounce", "pound", "gram", "kilogram", "metric ton", "liter", "milliliter"]

# yum yum
ingredient_adjs = ["chocolate", "banana", "strawberry", "pistachio", "almond", "orange", "lemon",
                    "chilli", "ube", "ice cream", "ice", "raspberry", "redberry", "wildberry",
                    "blackberry", "blueberry", "radiation", "yam", "dark", "milk", "white",
                   "brown", "caramelized", "incinerated", "opened", "expired"]
ingredient_nouns = ["cake mix", "chocolate", "chocolate wrappers", "yeast", "uranium",
                    "sugar", "water", "milk", "wheat", "barley", "eggs", "flour", "zest",
                    "pulp", "[UNKNOWN]"]

for i in range(rand.randint(5,15)):
    print("-",
          rand.choice(numbers), 
          round(rand.uniform(1,10), 2), 
          rand.choice(units), 
          rand.choice(ingredient_adjs),
          rand.choice(ingredient_nouns))

print("- "*25)
print("Please do not attempt to consume the finished serving.")
