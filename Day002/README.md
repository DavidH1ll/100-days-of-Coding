# Day 2 - Data Types & Mathematical Operations

## Overview
Day 2 focuses on working with different data types, type conversion, and performing mathematical calculations in Python.

## Project: Tip Calculator

A practical program that calculates how much each person should pay when splitting a bill, including tip.

### Features
- Calculates total bill with tip
- Splits the bill among multiple people
- Shows detailed breakdown:
  - Bill per person
  - Tip per person
  - Total per person
- Includes error handling for invalid inputs
- Formats currency to 2 decimal places

### What You'll Learn

**Data Types**:
- `int` - Whole numbers (number of people)
- `float` - Decimal numbers (bill amount, tip percentage)
- `str` - Text strings (for display)

**Mathematical Operations**:
- Addition (`+`) - Total bill calculation
- Division (`/`) - Splitting among people
- Multiplication (`*`) - Calculating tip amount
- Percentage calculations

**String Formatting**:
- f-strings with formatting (`{total:.2f}` for 2 decimal places)
- Displaying currency values

**Error Handling**:
- `try-except` blocks
- Catching `ValueError` for invalid inputs
- Validating positive numbers

## Usage

```powershell
python tipcalculator.py
```

### Example Session

```
Welcome to the Tip Calculator!
What is your bill total? $150.00
What percentage tip would you like to give? (10, 15, 20): 15
How many people are splitting the bill? 5

--- Summary ---
Bill Amount: $150.00
Tip Percentage: 15.0%
Tip Amount: $22.50
Total Amount: $172.50

--- Per Person ---
Bill per person: $30.00
Tip per person: $4.50
Total per person: $34.50
```

## Key Concepts Covered

1. **Type Conversion**
   - `float()` - Convert input to decimal number
   - `int()` - Convert input to whole number
   - `.2f` - Format number to 2 decimal places

2. **Mathematical Operations**
   - Percentage calculation: `bill * (tip_percent / 100)`
   - Division: `total / num_people`

3. **Error Handling**
   - Try-except blocks for robust input handling
   - Custom error messages

4. **Functions**
   - Defining functions with `def`
   - Using `if __name__ == "__main__":` pattern

## Running the Code

From the repository root:
```powershell
python .\Day002\tipcalculator.py
```

Or navigate to the Day002 directory:
```powershell
cd Day002
python tipcalculator.py
```

## Challenges & Extensions

Try enhancing the calculator:
- Add support for different currencies
- Save calculation history to a file
- Add a loop to calculate multiple bills
- Include tax calculation before tip
- Add option for custom tip percentages beyond 10/15/20

## Learning Resources

- [Python Data Types](https://docs.python.org/3/library/stdtypes.html)
- [Python Mathematical Operations](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [String Formatting](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
- [Error Handling with try-except](https://docs.python.org/3/tutorial/errors.html)
