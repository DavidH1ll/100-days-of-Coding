import os
from time import sleep

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

DRINK_ART = {
    "espresso": """
  (  )    
 :----:
C|====| 
 |    |
 `----'
    """,
    
    "latte": """
      )  (
     (   ) )
      ) ( (
    _______)_
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'
    """,
    
    "cappuccino": """
    (  )   (   )  )
     ) (   )  (  (
     ( )  (    ) )
     _____________
    <_____________> ___
    |             |/ _ _
    |               | | |
    |               |_| |
 ___|             |\___/
/    \___________/    }
\_____________________/'
    """
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

MACHINE_CAPACITY = {
    "water": 300,
    "milk": 200, 
    "coffee": 100
}

profit = 0

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_resources(drink_ingredients):
    """Check if there are sufficient resources to make the drink."""
    for item, amount in drink_ingredients.items():
        if resources[item] < amount:
            print(f"Sorry, not enough {item}.")
            return False
    return True

def process_coins():
    """Returns total calculated from coins inserted or None if invalid input."""
    print("Please insert coins.")
    total = 0
    
    try:
        quarters = int(input("How many quarters?: "))
        dimes = int(input("How many dimes?: "))
        nickles = int(input("How many nickles?: "))
        pennies = int(input("How many pennies?: "))
        
        if quarters < 0 or dimes < 0 or nickles < 0 or pennies < 0:
            raise ValueError("Coin amounts cannot be negative")
            
        total = (quarters * 0.25) + (dimes * 0.10) + (nickles * 0.05) + (pennies * 0.01)
        return total
        
    except ValueError:
        print("Invalid coin amount. Please enter positive numbers only.")
        return None

def display_drink_art(drink_name):
    """Display ASCII art for the selected drink."""
    if drink_name in DRINK_ART:
        print(DRINK_ART[drink_name])

def make_coffee(drink_name, drink_ingredients, change=0):
    """Deduct resources, show drink art, then display change after delay."""
    # Deduct ingredients
    for item, amount in drink_ingredients.items():
        resources[item] -= amount
    
    clear_screen()
    print(f"\nHere is your {drink_name}. Enjoy!")
    
    # Show drink art
    if drink_name in DRINK_ART:
        print(DRINK_ART[drink_name])
        
    
    # Show change if any
    if change > 0:
        print(f"\nHere is ${change:.2f} in change.")

def print_report():
    """Print current resource levels and profit."""
    clear_screen()
    print("\n----- Machine Report -----")
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml") 
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit:.2f}")
    print("-----------------------\n")

def refill_machine():
    """Refill all resources to maximum capacity."""
    global resources
    resources = MACHINE_CAPACITY.copy()
    print("\n----- Machine Refilled -----")
    print("All resources restored to maximum capacity:")
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print("--------------------------\n")

def display_menu():
    """Display numbered menu options."""
    clear_screen()
    print("\n----- COFFEE MACHINE MENU -----")
    print("1. Espresso    ($1.50)")
    print("2. Latte       ($2.50)")
    print("3. Cappuccino  ($3.00)")
    print("----------------------------")

def get_drink_choice(choice):
    """Convert numeric choice to drink name."""
    menu_options = {
        "1": "espresso",
        "2": "latte",
        "3": "cappuccino",
        "4": "report",
        "5": "refill",
        "6": "off"
    }
    return menu_options.get(choice, "invalid")

def coffee_machine():
    global profit
    machine_on = True

    while machine_on:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")
        action = get_drink_choice(choice)
        clear_screen()
        
        if action == "off":
            machine_on = False
        elif action == "report":
            print_report()
        elif action == "refill":
            refill_machine()
        elif action in MENU:
            drink = MENU[action]
            if check_resources(drink["ingredients"]):
                payment = process_coins()
                if payment is None:
                    print("Transaction cancelled due to invalid payment.")
                elif payment >= drink["cost"]:
                    change = round(payment - drink["cost"], 2)
                    profit += drink["cost"]
                    make_coffee(action, drink["ingredients"], change)
                else:
                    print("Sorry that's not enough money. Money refunded.")
        else:
            print("Invalid selection. Please try again.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    coffee_machine()