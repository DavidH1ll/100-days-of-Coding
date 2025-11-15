# Day 3 - Conditional Statements & Control Flow

## Overview
Day 3 introduces conditional logic with `if`, `elif`, and `else` statements. Learn to create programs that make decisions based on user input and conditions.

## Projects

### 1. BMI Calculator (`challenge.py`)
Calculates Body Mass Index and provides health category interpretation.

**Features**:
- Converts height from cm to meters
- Calculates BMI using formula: `weight / height²`
- Categorizes results (underweight, normal, overweight)
- Input validation and error handling

**Usage**:
```powershell
python challenge.py
```

**Example**:
```
Enter your weight in kg: 70
Enter your height in cm: 175
Your BMI is 22.9, you have normal weight
```

**Key Concepts**:
- Multiple conditional branches (`if-elif-else`)
- Comparison operators (`<`, `>=`)
- Exponentiation (`**`)

---

### 2. Pizza Delivery Calculator (`pizza_delivery.py`)
Calculates the total cost of a pizza order with customizable toppings.

**Pricing**:
- Small (S): $15 + $2 for pepperoni
- Medium (M): $20 + $3 for pepperoni
- Large (L): $25 + $3 for pepperoni
- Extra cheese: +$1 (any size)

**Features**:
- Input validation with loops
- Order summary display
- Dynamic pricing based on selections

**Usage**:
```powershell
python pizza_delivery.py
```

**Example Session**:
```
Welcome to Python Pizza Deliveries!
What size pizza do you want? (S/M/L): L
Do you want pepperoni? (Y/N): Y
Do you want extra cheese? (Y/N): N

--- Order Summary ---
Size: Large
Pepperoni: Yes
Extra cheese: No
Total price: $28.00
```

**Key Concepts**:
- Nested conditionals
- Input validation loops
- Variable accumulation

---

### 3. Rollercoaster Ticket System (`rollercoaster.py`)
Theme park ticketing system with age-based pricing and photo options.

**Pricing Structure**:
- Children (< 12): $5
- Teens (12-17): $7
- Adults (18-44, 56+): $12
- Free for ages 45-55!
- Photo add-on: +$3

**Features**:
- Height requirement check (minimum 120cm)
- Age-based pricing tiers
- Optional photo purchase
- Complete order summary
- Graceful exit option

**Usage**:
```powershell
python rollercoaster.py
```

**Example**:
```
Welcome to the Theme Park Ticket System!
Enter your height in cm: 150
Enter your age: 25
Do you want a photo? (Y/N): Y

--- Ticket Summary ---
Ticket price: $12.00
Photo: $3.00
Total: $15.00
Enjoy your ride!
```

**Key Concepts**:
- Early returns for failed conditions
- Multiple pricing tiers
- Combined conditional logic

---

### 4. Treasure Island Game (`TreasureIsland.py`) 🏴‍☠️
Interactive text-based adventure game where you navigate to find treasure.

**Features**:
- ASCII art introduction
- Multiple choice pathways
- Win/lose scenarios based on decisions
- Simple game logic demonstration

**How to Play**:
1. Choose left or right at the crossroad
2. Decide to wait or swim at the lake
3. Pick a colored door (red, yellow, or blue)

**Winning Path**: Left → Wait → Yellow door

**Usage**:
```powershell
python TreasureIsland.py
```

**Example Gameplay**:
```
Welcome to Treasure Island!
Your mission is to find the treasure.
You're at a crossroads. Where do you want to go? Type "left" or "right"
> left
You've come to a lake. Type "wait" to wait for a boat. Type "swim" to swim across.
> wait
Which colour door do you choose? (red/yellow/blue)
> yellow
You found the treasure! You Win!
```

**Key Concepts**:
- Nested if-else structures
- String methods (`.lower()`)
- Sequential decision trees
- Game flow control

---

## Key Concepts Covered

### Comparison Operators
- `==` Equal to
- `!=` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal to
- `<=` Less than or equal to

### Logical Operators
- `and` - Both conditions must be true
- `or` - At least one condition must be true
- `not` - Inverts the condition

### Control Flow Structures
```python
# Simple if
if condition:
    # code

# If-else
if condition:
    # code
else:
    # alternative code

# If-elif-else
if condition1:
    # code
elif condition2:
    # code
else:
    # fallback code

# Nested conditions
if outer_condition:
    if inner_condition:
        # code
```

## Running the Projects

From the repository root:
```powershell
# BMI Calculator
python .\Day003\challenge.py

# Pizza Delivery
python .\Day003\pizza_delivery.py

# Rollercoaster Tickets
python .\Day003\rollercoaster.py

# Treasure Island Game
python .\Day003\TreasureIsland.py
```

Or navigate to Day003:
```powershell
cd Day003
python challenge.py
python pizza_delivery.py
python rollercoaster.py
python TreasureIsland.py
```

## Challenges & Extensions

Try enhancing these projects:
- **BMI Calculator**: Add more BMI categories (severely underweight, obese, etc.)
- **Pizza Delivery**: Add more toppings, drink options, or delivery fee
- **Rollercoaster**: Add family packages, season passes, or group discounts
- **Treasure Island**: Create more branching paths, add inventory system, include random events

## Learning Resources

- [Python if-elif-else](https://docs.python.org/3/tutorial/controlflow.html#if-statements)
- [Comparison Operators](https://docs.python.org/3/library/stdtypes.html#comparisons)
- [Logical Operators](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)
- [Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
