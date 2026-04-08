import random


class CakeRecipeGenerator:
    def __init__(self):
        self.cake_bases = [
            "vanilla", "chocolate", "red velvet", "carrot", "lemon",
            "strawberry", "cheesecake", "tiramisu", "black forest"
        ]
        
        self.cake_sizes = ["6-inch", "8-inch", "10-inch", "sheet cake"]
        
        self.frostings = [
            "buttercream", "cream cheese frosting", "ganache",
            "whipped cream", "Italian meringue", "salted caramel"
        ]
        
        self.frosting_flavors = [
            "vanilla", "chocolate", "raspberry", "lemon",
            "coffee", "coconut", "mint", "maple"
        ]
        
        self.toppings = [
            "sprinkles", "edible glitter", "crushed cookies", "toasted nuts",
            "fresh berries", "chocolate chips", "caramel drizzle", "fondant flowers",
            "chopped candy", "coconut flakes", "candied fruit"
        ]
        
        self.special_ingredients = [
            "espresso powder", "orange zest", "almond extract", "rum",
            "vanilla bean", "sea salt", "cardamom", "cinnamon"
        ]
    
    def generate_recipe(self):
        cake_base = random.choice(self.cake_bases)
        cake_size = random.choice(self.cake_sizes)
        frosting = random.choice(self.frostings)
        frosting_flavor = random.choice(self.frosting_flavors)
        toppings = random.sample(self.toppings, k=random.randint(1, 3))
        special_ingredient = random.choice(self.special_ingredients) if random.random() > 0.4 else None
        
        recipe = {
            "base": cake_base,
            "size": cake_size,
            "frosting": frosting,
            "frosting_flavor": frosting_flavor,
            "toppings": toppings,
            "special_ingredient": special_ingredient
        }
        
        return recipe
    
    def format_recipe(self, recipe):
        output = []
        output.append("=" * 50)
        output.append("🍰 RANDOMLY GENERATED CAKE RECIPE 🍰".center(50))
        output.append("=" * 50)
        output.append("")
        output.append(f"Base Cake:        {recipe['base'].title()}")
        output.append(f"Size:             {recipe['size']}")
        output.append(f"Frosting:         {recipe['frosting'].title()}")
        output.append(f"Frosting Flavor:  {recipe['frosting_flavor'].title()}")
        output.append(f"Toppings:         {', '.join(t.title() for t in recipe['toppings'])}")
        
        if recipe['special_ingredient']:
            output.append(f"Special Touch:    Add a hint of {recipe['special_ingredient']}")
        
        output.append("")
        output.append("=" * 50)
        
        return "\n".join(output)
    
    def generate_and_display(self):
        recipe = self.generate_recipe()
        return self.format_recipe(recipe)


def main():
    generator = CakeRecipeGenerator()
    
    print("Welcome to the Random Cake Recipe Generator!\n")
    
    while True:
        print(generator.generate_and_display())
        
        user_input = input("\nGenerate another recipe? (y/n): ").strip().lower()
        if user_input != 'y':
            print("\nHappy baking! 🍰")
            break
        print()


if __name__ == "__main__":
    main()
