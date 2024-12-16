from prettytable import PrettyTable
import os
from time import sleep
from dataclasses import dataclass
from typing import Dict, Optional

DRINK_ART = {
    "espresso": """
      ) (  
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

@dataclass
class MenuItem:
    name: str
    water: int
    coffee: int
    milk: int
    cost: float
    art: str

class MoneyMachine:
    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01
    }
    
    def __init__(self):
        self.profit = 0
        
    def process_coins(self) -> Optional[float]:
        print("Please insert coins.")
        total = 0
        
        try:
            for coin, value in self.COIN_VALUES.items():
                count = int(input(f"How many {coin}?: "))
                if count < 0:
                    raise ValueError("Coin amounts cannot be negative")
                total += count * value
            return total
        except ValueError:
            print("Invalid coin amount. Please enter positive numbers only.")
            return None

class CoffeeMachine:
    def __init__(self):
        self.money_machine = MoneyMachine()
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100
        }
        self.menu_items = {
            "1": MenuItem("espresso", 50, 18, 0, 1.5, DRINK_ART["espresso"]),
            "2": MenuItem("latte", 200, 24, 150, 2.5, DRINK_ART["latte"]),
            "3": MenuItem("cappuccino", 250, 24, 100, 3.0, DRINK_ART["cappuccino"])
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def check_resources(self, drink: MenuItem) -> bool:
        for item, amount in {
            "water": drink.water,
            "coffee": drink.coffee,
            "milk": drink.milk
        }.items():
            if self.resources[item] < amount:
                print(f"Sorry, not enough {item}.")
                return False
        return True
    
    def make_coffee(self, drink: MenuItem, change: float = 0):
        self.resources["water"] -= drink.water
        self.resources["coffee"] -= drink.coffee
        self.resources["milk"] -= drink.milk
        
        self.clear_screen()
        print(f"\nHere is your {drink.name}. Enjoy!")
        print(drink.art)
        
        if change > 0:
            print(f"\nHere is ${change:.2f} in change.")
    
    def display_menu(self):
        self.clear_screen()
        table = PrettyTable()
        table.title = "COFFEE MACHINE MENU"
        table.field_names = ["Choice", "Drink", "Price", "Water", "Coffee", "Milk"]
        
        for key, item in self.menu_items.items():
            table.add_row([
                key,
                item.name.capitalize(),
                f"${item.cost:.2f}",
                f"{item.water}ml",
                f"{item.coffee}g",
                f"{item.milk}ml"
            ])
        
        table.add_row(["4", "Report", "-", "-", "-", "-"])
        table.add_row(["5", "Refill", "-", "-", "-", "-"])
        table.add_row(["6", "Off", "-", "-", "-", "-"])
        
        print(table)
    
    def print_report(self):
        self.clear_screen()
        table = PrettyTable()
        table.title = "MACHINE REPORT"
        table.field_names = ["Resource", "Amount"]
        
        table.add_row(["Water", f"{self.resources['water']}ml"])
        table.add_row(["Milk", f"{self.resources['milk']}ml"])
        table.add_row(["Coffee", f"{self.resources['coffee']}g"])
        table.add_row(["Money", f"${self.money_machine.profit:.2f}"])
        
        print(table)
    
    def refill(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100
        }
        table = PrettyTable()
        table.title = "MACHINE REFILLED"
        table.field_names = ["Resource", "New Amount"]
        
        table.add_row(["Water", f"{self.resources['water']}ml"])
        table.add_row(["Milk", f"{self.resources['milk']}ml"])
        table.add_row(["Coffee", f"{self.resources['coffee']}g"])
        
        print(table)

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "6":
                break
            elif choice == "4":
                self.print_report()
            elif choice == "5":
                self.refill()
            elif choice in self.menu_items:
                drink = self.menu_items[choice]
                if self.check_resources(drink):
                    payment = self.money_machine.process_coins()
                    if payment is not None:
                        if payment >= drink.cost:
                            change = round(payment - drink.cost, 2)
                            self.money_machine.profit += drink.cost
                            self.make_coffee(drink, change)
                        else:
                            print("Sorry that's not enough money. Money refunded.")
            else:
                print("Invalid selection. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    coffee_machine = CoffeeMachine()
    coffee_machine.run()