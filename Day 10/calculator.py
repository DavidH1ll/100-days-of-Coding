import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Calculator logo
logo = """
 _____________________
|  _________________  |
| | Python Calc   0.| |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|
"""

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2 if n2 != 0 else "Error: Division by zero"

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

def calculator():
    clear_screen()
    print(logo)
    
    try:
        num1 = float(input("Enter first number: "))
        should_continue = True
        
        while should_continue:
            print("\nAvailable operations:")
            for symbol in operations:
                print(symbol)
                
            operation_symbol = input("Pick an operation: ")
            num2 = float(input("Enter next number: "))
            
            if operation_symbol in operations:
                calculation_function = operations[operation_symbol]
                result = calculation_function(num1, num2)
                
                print(f"\n{num1} {operation_symbol} {num2} = {result}")
                
                if input(f"\nContinue calculating with {result}? (y/n): ").lower() == 'y':
                    num1 = result
                else:
                    should_continue = False
                    calculator()  # Start fresh calculation
            else:
                print("Invalid operation!")
                
    except ValueError:
        print("Please enter valid numbers!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    calculator()