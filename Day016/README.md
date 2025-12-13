# Day 16 – Object-Oriented Coffee Machine

## Overview
Refactored the procedural coffee machine (Day 15) into an object-oriented design to improve readability, extensibility, and testability.

## Files
- OOCoffeeMachine.py – classes for MenuItem, Menu, CoffeeMaker, MoneyMachine.
- main.py – orchestrates user interaction using the above classes.
- exercise.py – supporting OOP practice (attributes, methods).

## Concepts Practiced
- Class design (responsibility separation).
- Encapsulation of state (resources, money).
- Reuse via composition (main script coordinates objects).
- Data modeling (MenuItem for drink definition).
- Methods vs functions (behavior bound to objects).

## How It Works
1. Menu lists drinks (name, ingredients, cost).
2. CoffeeMaker checks and deducts resources.
3. MoneyMachine processes coin input and tracks profit.
4. Loop continues until user types `off`; `report` prints status.

## Run
```bash
python main.py