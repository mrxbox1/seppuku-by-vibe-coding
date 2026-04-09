import random


class AdvancedCakeRecipeGenerator:
    def __init__(self):
        self.cake_bases = [
            "vanilla", "chocolate", "red velvet", "carrot", "lemon",
            "strawberry", "cheesecake", "tiramisu", "black forest",
            "funfetti", "coconut", "espresso", "lavender", "matcha",
            "honey cake", "almond", "pistachio"
        ]
        
        self.cake_sizes = {
            "6-inch": {"servings": 6, "bake_time": 25},
            "8-inch": {"servings": 12, "bake_time": 30},
            "10-inch": {"servings": 16, "bake_time": 35},
            "sheet cake": {"servings": 20, "bake_time": 35}
        }
        
        self.frostings = [
            "buttercream", "cream cheese frosting", "ganache",
            "whipped cream", "Italian meringue", "salted caramel",
            "Swiss meringue", "mascarpone cream", "ermine frosting",
            "mousse frosting", "American buttercream", "French buttercream"
        ]
        
        self.frosting_flavors = [
            "vanilla", "chocolate", "raspberry", "lemon", "coffee",
            "coconut", "mint", "maple", "passion fruit", "pistachio",
            "caramel", "salted caramel", "toffee", "bananas foster", "eggnog"
        ]
        
        self.toppings = [
            "sprinkles", "edible glitter", "crushed cookies", "toasted nuts",
            "fresh berries", "chocolate chips", "caramel drizzle", "fondant flowers",
            "chopped candy", "coconut flakes", "candied fruit", "gold leaf",
            "crushed macarons", "chocolate shavings", "fresh whipped cream",
            "dried flowers", "marzipan decorations"
        ]
        
        self.special_ingredients = [
            "espresso powder", "orange zest", "almond extract", "rum",
            "vanilla bean", "sea salt", "cardamom", "cinnamon",
            "rose water", "matcha powder", "balsamic vinegar", "maple syrup",
            "bourbon", "cointreau", "lavender extract", "peppermint extract"
        ]
        
        self.base_ingredients = {
            "vanilla": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "vanilla extract": "2 tsp",
                "baking powder": "2 tsp",
                "salt": "0.5 tsp",
                "whole milk": "0.75 cup"
            },
            "chocolate": {
                "all-purpose flour": "1.75 cups",
                "unsweetened cocoa powder": "0.75 cup",
                "granulated sugar": "2 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "vanilla extract": "1 tsp",
                "baking powder": "1.5 tsp",
                "baking soda": "0.5 tsp",
                "salt": "0.5 tsp",
                "hot water": "0.5 cup"
            },
            "lemon": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "fresh lemon zest": "2 tbsp",
                "fresh lemon juice": "0.25 cup",
                "baking powder": "2 tsp",
                "salt": "0.5 tsp",
                "whole milk": "0.75 cup"
            },
            "strawberry": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "fresh strawberry puree": "0.5 cup",
                "vanilla extract": "1 tsp",
                "baking powder": "2 tsp",
                "salt": "0.5 tsp",
                "whole milk": "0.5 cup"
            },
            "carrot": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "vegetable oil": "0.75 cup",
                "large eggs": "3",
                "grated carrots": "1.5 cups",
                "crushed pineapple (drained)": "0.5 cup",
                "baking powder": "1.5 tsp",
                "baking soda": "1 tsp",
                "ground cinnamon": "2 tsp",
                "salt": "0.5 tsp"
            },
            "coconut": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "coconut milk": "0.75 cup",
                "shredded coconut": "1 cup",
                "coconut extract": "1 tsp",
                "baking powder": "2 tsp",
                "salt": "0.5 tsp"
            },
            "espresso": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.75 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "espresso powder": "2 tbsp",
                "hot water": "0.5 cup",
                "vanilla extract": "1 tsp",
                "baking powder": "1.5 tsp",
                "baking soda": "0.5 tsp",
                "salt": "0.5 tsp"
            },
            "lavender": {
                "all-purpose flour": "2 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.75 cup",
                "large eggs": "3",
                "dried lavender buds": "1 tbsp",
                "vanilla extract": "1 tsp",
                "baking powder": "2 tsp",
                "salt": "0.5 tsp",
                "whole milk": "0.75 cup"
            },
            "red velvet": {
                "all-purpose flour": "2.5 cups",
                "granulated sugar": "1.5 cups",
                "unsalted butter": "0.5 cup",
                "large eggs": "2",
                "red food coloring": "1-2 oz",
                "unsweetened cocoa powder": "2 tbsp",
                "buttermilk": "1 cup",
                "white vinegar": "1 tbsp",
                "vanilla extract": "1 tsp",
                "baking soda": "1 tsp",
                "salt": "0.5 tsp"
            }
        }
    
    def get_size_multiplier(self, size):
        sizes = {
            "6-inch": 0.5,
            "8-inch": 1.0,
            "10-inch": 1.5,
            "sheet cake": 2.0
        }
        return sizes.get(size, 1.0)
    
    def scale_ingredients(self, ingredients, multiplier):
        scaled = {}
        for ingredient, amount in ingredients.items():
            parts = amount.split()
            try:
                quantity = float(parts[0])
                scaled[ingredient] = f"{quantity * multiplier:.2g} {' '.join(parts[1:])}"
            except (ValueError, IndexError):
                scaled[ingredient] = amount
        return scaled
    
    def get_base_ingredients(self, cake_type, size):
        base_ingredients = self.base_ingredients.get(
            cake_type,
            self.base_ingredients["vanilla"]
        )
        multiplier = self.get_size_multiplier(size)
        return self.scale_ingredients(base_ingredients, multiplier)
    
    def generate_frosting_ingredients(self, frosting_type, flavor, size):
        multiplier = self.get_size_multiplier(size)
        
        frosting_bases = {
            "buttercream": {
                "unsalted butter": f"{1.5 * multiplier:.1f} cups",
                "powdered sugar": f"{4 * multiplier:.1f} cups",
                "vanilla extract": "1 tsp",
                "whole milk": "2-3 tbsp"
            },
            "cream cheese frosting": {
                "cream cheese (softened)": f"{8 * multiplier:.0f} oz",
                "unsalted butter": f"{0.5 * multiplier:.1f} cup",
                "powdered sugar": f"{2 * multiplier:.1f} cups",
                "vanilla extract": "1 tsp"
            },
            "ganache": {
                "dark chocolate (chopped)": f"{8 * multiplier:.0f} oz",
                "heavy cream": f"{1 * multiplier:.1f} cup",
                "unsalted butter": f"{2 * multiplier:.0f} tbsp"
            },
            "whipped cream": {
                "heavy cream (chilled)": f"{2 * multiplier:.1f} cups",
                "powdered sugar": f"{3 * multiplier:.0f} tbsp",
                "vanilla extract": "0.5 tsp"
            },
            "Swiss meringue": {
                "egg whites": f"{5 * multiplier:.0f}",
                "granulated sugar": f"{1.25 * multiplier:.2f} cups",
                "unsalted butter": f"{1 * multiplier:.1f} cup",
                "vanilla extract": "1 tsp",
                "salt": "pinch"
            },
            "mascarpone cream": {
                "mascarpone cheese": f"{1 * multiplier:.1f} cups",
                "heavy cream": f"{0.5 * multiplier:.1f} cup",
                "powdered sugar": f"{0.5 * multiplier:.1f} cup",
                "vanilla extract": "1 tsp"
            }
        }
        
        return frosting_bases.get(frosting_type, frosting_bases["buttercream"])
    
    def generate_instructions(self, cake_base, special_ingredient):
        instructions = [
            "PREP:",
            "1. Preheat oven to 350°F (175°C).",
            "2. Prepare your cake pan(s) by greasing and flouring, or lining with parchment paper.",
            "3. Allow all ingredients to come to room temperature for better mixing.",
            "",
            "DRY INGREDIENTS:",
            "4. In a medium bowl, sift together flour, baking powder, baking soda (if applicable), and salt.",
            "5. Whisk the dry mixture for 10 seconds to ensure even distribution.",
            "",
            "WET INGREDIENTS:",
            "6. In a large bowl, cream together butter and sugar until light and fluffy (2-3 minutes).",
            "7. Beat in eggs one at a time, ensuring each egg is fully incorporated before adding the next.",
            "8. Gently mix in vanilla extract or other vanilla products.",
            "",
            "COMBINING:",
            "9. Alternate adding dry ingredients and wet ingredients (milk, water, or other liquids) to the butter mixture.",
            "10. Start with dry ingredients, then wet, then dry again, and end with dry.",
            "11. Mix on low speed after each addition until just combined. Do not overmix.",
            "",
        ]
        
        if special_ingredient:
            instructions.append(f"12. Gently fold in {special_ingredient} to taste.")
            instructions.append("")
        
        instructions.extend([
            "BAKING:",
            "13. Pour batter evenly into prepared pan(s) and smooth the top.",
            "14. Tap the pan on the counter once or twice to release air bubbles.",
            "15. Place in preheated oven and bake until a toothpick inserted in the center comes out clean.",
            "16. This typically takes 25-35 minutes depending on pan size.",
            "17. The cake should be golden brown on the edges and spring back when lightly touched.",
            "",
            "COOLING:",
            "18. Remove from oven and allow to cool in the pan for 10-15 minutes.",
            "19. Turn out onto a wire cooling rack and cool completely (at least 1-2 hours).",
            "20. Make sure the cake is completely cool before frosting to prevent melting.",
            "",
            "FROSTING:",
            "21. Prepare your frosting by combining all ingredients in a bowl.",
            "22. Mix on medium speed until smooth and fluffy (2-3 minutes).",
            "23. If frosting is too thick, add milk or cream 1 tbsp at a time.",
            "24. If frosting is too thin, add more powdered sugar 1 tbsp at a time.",
            "",
            "ASSEMBLY:",
            "25. Place cake on a cake board or serving plate.",
            "26. Apply a thin 'crumb coat' of frosting and chill for 15 minutes.",
            "27. Apply the final generous layer of frosting.",
            "28. Use an offset spatula to smooth or create texture as desired.",
            "29. Pipe decorative elements if you wish.",
            "",
            "DECORATING:",
            "30. Add your chosen toppings while frosting is still slightly tacky.",
            "31. Chill the finished cake for at least 30 minutes before serving.",
            "32. Remove from refrigerator 15-20 minutes before serving for best flavor.",
            "33. Slice with a hot, wet knife for clean cuts.",
            "34. Serve and enjoy! 🍰"
        ])
        
        return instructions
    
    def generate_recipe(self):
        cake_base = random.choice(self.cake_bases)
        cake_size = random.choice(list(self.cake_sizes.keys()))
        frosting = random.choice(self.frostings)
        frosting_flavor = random.choice(self.frosting_flavors)
        toppings = random.sample(self.toppings, k=random.randint(1, 4))
        special_ingredient = random.choice(self.special_ingredients) if random.random() > 0.3 else None
        
        base_ingredients = self.get_base_ingredients(cake_base, cake_size)
        frosting_ingredients = self.generate_frosting_ingredients(frosting, frosting_flavor, cake_size)
        instructions = self.generate_instructions(cake_base, special_ingredient)
        
        recipe = {
            "base": cake_base,
            "size": cake_size,
            "servings": self.cake_sizes[cake_size]["servings"],
            "bake_time": self.cake_sizes[cake_size]["bake_time"],
            "frosting": frosting,
            "frosting_flavor": frosting_flavor,
            "toppings": toppings,
            "special_ingredient": special_ingredient,
            "base_ingredients": base_ingredients,
            "frosting_ingredients": frosting_ingredients,
            "instructions": instructions
        }
        
        return recipe
    
    def format_recipe(self, recipe):
        output = []
        output.append("=" * 70)
        output.append("🍰 RANDOMLY GENERATED CAKE RECIPE 🍰".center(70))
        output.append("=" * 70)
        output.append("")
        
        output.append(f"CAKE TYPE:        {recipe['base'].title()}")
        output.append(f"SIZE:             {recipe['size']}")
        output.append(f"SERVINGS:         {recipe['servings']} servings")
        output.append(f"BAKE TIME:        {recipe['bake_time']} minutes")
        output.append("")
        
        output.append("📝 CAKE INGREDIENTS:")
        output.append("-" * 70)
        for ingredient, amount in recipe['base_ingredients'].items():
            output.append(f"  • {ingredient.title():<40} {amount}")
        
        if recipe['special_ingredient']:
            output.append(f"  • {recipe['special_ingredient'].title():<40} To taste")
        
        output.append("")
        output.append(f"🧁 FROSTING ({recipe['frosting'].title()} - {recipe['frosting_flavor'].title()}):")
        output.append("-" * 70)
        for ingredient, amount in recipe['frosting_ingredients'].items():
            output.append(f"  • {ingredient.title():<40} {amount}")
        
        output.append("")
        output.append("✨ TOPPINGS:")
        output.append("-" * 70)
        for topping in recipe['toppings']:
            output.append(f"  • {topping.title()}")
        
        output.append("")
        output.append("👨‍🍳 DETAILED INSTRUCTIONS:")
        output.append("-" * 70)
        for instruction in recipe['instructions']:
            output.append(f"  {instruction}")
        
        output.append("")
        output.append("=" * 70)
        output.append("Happy baking! 🎉".center(70))
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def generate_and_display(self):
        recipe = self.generate_recipe()
        return self.format_recipe(recipe)


def main():
    generator = AdvancedCakeRecipeGenerator()
    
    print("\n" + "=" * 70)
    print("🎂 Welcome to the Advanced Random Cake Recipe Generator! 🎂".center(70))
    print("=" * 70)
    print("\nThis generator creates unique cake recipes with ingredients and")
    print("detailed instructions. Every recipe is randomly generated from a")
    print("combination of cake types, frostings, and toppings.\n")
    
    recipe_count = 0
    
    while True:
        print(generator.generate_and_display())
        recipe_count += 1
        
        user_input = input("\nGenerate another recipe? (y/n): ").strip().lower()
        if user_input != 'y':
            print(f"\n{'=' * 70}")
            print(f"You generated {recipe_count} delicious cake recipe(ies)!".center(70))
            print("Happy baking! 🍰".center(70))
            print(f"{'=' * 70}\n")
            break
        print()


if __name__ == "__main__":
    main()
