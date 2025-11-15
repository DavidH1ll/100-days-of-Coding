# Day 9 - Dictionaries & Nesting

## Overview
Day 9 introduces dictionaries, Python's key-value pair data structure, and the concept of nesting (dictionaries within dictionaries, lists within dictionaries). Learn to organize complex data and build a real-world auction application.

## Projects

### 1. Nested Dictionaries Practice (`exercises.py`)

Demonstrates working with nested data structures - dictionaries containing dictionaries and lists.

#### Data Structure

```python
travel_log = {
    "France": {
        "capital": "Paris",
        "visited_cities": ["Lyon", "Marseille", "Nice"]
    },
    "Germany": {
        "capital": "Berlin",
        "visited_cities": ["Munich", "Hamburg", "Frankfurt"]
    }
    # ... more countries
}
```

#### Accessing Nested Data

```python
# Access country's capital
travel_log["France"]["capital"]  # "Paris"

# Access specific city in list
travel_log["Japan"]["visited_cities"][1]  # "Kyoto"
```

**Key Concepts**:
- Nested dictionaries (dict within dict)
- Lists as dictionary values
- Multi-level data access with bracket notation

**Usage**:
```powershell
python exercises.py
```

---

### 2. Silent Auction Program (`silent_auction.py`)

A complete blind auction system where bidders submit bids privately and the highest bidder wins.

#### Features

✅ **ASCII Art Logo**: Attractive auction gavel display  
✅ **Private Bidding**: Screen clears between bidders  
✅ **Multiple Bidders**: Unlimited participants  
✅ **Automatic Winner**: Finds highest bid  
✅ **Winner Banner**: Celebratory ASCII art announcement  
✅ **Input Validation**: Handles invalid bid amounts  
✅ **Formatted Output**: Currency display with 2 decimal places  

#### How It Works

1. **Display Logo**: Shows auction gavel
2. **Collect Bids**: 
   - Enter bidder name
   - Enter bid amount
   - Ask if more bidders
3. **Clear Screen**: Hide previous bids (silent auction)
4. **Repeat**: Until no more bidders
5. **Find Winner**: Determine highest bid
6. **Display Result**: Show winner with celebration banner

#### Usage

```powershell
python silent_auction.py
```

#### Example Session

```
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\
                       .-------------.
                      /_______________\

Welcome to the Secret Auction Program!
What is your name?: Alice
What's your bid?: $250
Are there any other bidders? (yes/no): yes

[Screen clears]

What is your name?: Bob
What's your bid?: $300
Are there any other bidders? (yes/no): yes

What is your name?: Charlie
What's your bid?: $275
Are there any other bidders? (yes/no): no

╔══════════════════════════════════════════════════════════════╗
    🏆 BOB IS THE WINNER! 🏆                
║                                                              ║
║   ██╗    ██╗██╗███╗   ██╗███╗   ██╗███████╗██████╗ ██╗       ║
║   ██║    ██║██║████╗  ██║████╗  ██║██╔════╝██╔══██╗██║       ║
║   ██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝██║       ║
║   ██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗╚═╝       ║
║   ╚███╔███╔╝██║██║ ╚████║██║ ╚████║███████╗██║  ██║██╗       ║
║    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Winning bid: $300.00!
```

---

## Key Concepts Covered

### 1. Dictionaries Basics

#### Creating Dictionaries
```python
# Empty dictionary
my_dict = {}

# Dictionary with initial data
student = {
    "name": "Alice",
    "age": 20,
    "grade": "A"
}
```

#### Accessing Values
```python
print(student["name"])  # "Alice"
print(student.get("age"))  # 20
print(student.get("missing", "N/A"))  # "N/A" (default value)
```

#### Adding/Updating Values
```python
student["email"] = "alice@email.com"  # Add new key
student["age"] = 21  # Update existing key
```

#### Removing Values
```python
del student["grade"]  # Remove key-value pair
value = student.pop("age")  # Remove and return value
```

### 2. Dictionary Methods

```python
person = {"name": "Bob", "age": 25}

person.keys()      # dict_keys(['name', 'age'])
person.values()    # dict_values(['Bob', 25])
person.items()     # dict_items([('name', 'Bob'), ('age', 25)])

# Check if key exists
if "name" in person:
    print("Name exists")
```

### 3. Looping Through Dictionaries

```python
# Loop through keys
for key in student:
    print(key)

# Loop through values
for value in student.values():
    print(value)

# Loop through key-value pairs
for key, value in student.items():
    print(f"{key}: {value}")
```

### 4. Nesting Data Structures

#### List of Dictionaries
```python
students = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 87},
    {"name": "Charlie", "score": 92}
]

print(students[1]["name"])  # "Bob"
```

#### Dictionary of Dictionaries
```python
grades = {
    "Alice": {"math": 95, "science": 88},
    "Bob": {"math": 87, "science": 92}
}

print(grades["Alice"]["math"])  # 95
```

#### Dictionary with Lists
```python
contacts = {
    "Alice": ["alice@email.com", "555-1234"],
    "Bob": ["bob@email.com", "555-5678"]
}

print(contacts["Alice"][0])  # "alice@email.com"
```

### 5. Finding Max/Min in Dictionary

```python
bids = {"Alice": 250, "Bob": 300, "Charlie": 275}

# Find maximum value
max_bid = max(bids.values())  # 300

# Find key with maximum value
winner = max(bids, key=bids.get)  # "Bob"

# Alternative with items()
winner, amount = max(bids.items(), key=lambda x: x[1])
```

---

## Running the Projects

From the repository root:
```powershell
# Nested dictionaries practice
python .\Day009\exercises.py

# Silent auction
python .\Day009\silent_auction.py
```

Or navigate to Day009:
```powershell
cd Day009
python exercises.py
python silent_auction.py
```

---

## Challenges & Extensions

### Silent Auction Enhancements

**Easy**:
- Show all bids at the end (leaderboard)
- Add minimum bid requirement
- Display number of participants
- Add bid increment validation (must be higher than current highest)

**Medium**:
- **Tie Handling**: What if multiple people bid the same amount?
- **Reserve Price**: Minimum acceptable bid
- **Bid History**: Store timestamp with each bid
- **Save Results**: Write auction results to a file
- **Email Notifications**: Send winner notification
- **Starting Bid**: Set a starting price

**Advanced**:
- **Live Auction**: Real-time bidding with countdown timer
- **Multi-Item Auction**: Bid on different items
- **Proxy Bidding**: Auto-increment to beat others up to max
- **Sealed-Bid Auction**: Second-price auction (Vickrey)
- **Web Interface**: Flask/Django web app
- **Database Storage**: Use SQLite to store auction data
- **Authentication**: User accounts and login system

### Nested Data Structure Practice

**Create**:
- Student gradebook (students → courses → assignments → scores)
- Library catalog (books → authors, genres, ratings, reviews)
- Restaurant menu (categories → items → ingredients, prices)
- Family tree (generations → people → relationships)
- Music library (artists → albums → tracks → metadata)

---

## Dictionary vs List: When to Use?

| Feature | List | Dictionary |
|---------|------|------------|
| **Order** | Ordered (maintains insertion order) | Ordered (Python 3.7+) |
| **Access** | By index (0, 1, 2...) | By key (any immutable type) |
| **Lookup Speed** | O(n) - must search | O(1) - instant lookup |
| **Use When** | Ordered sequence, iteration | Key-value mapping, fast lookup |
| **Example** | Shopping list, high scores | Phone book, settings |

---

## Common Mistakes & Solutions

### ❌ KeyError When Key Doesn't Exist
```python
# Wrong - crashes if key missing
score = grades["David"]

# Better - use .get() with default
score = grades.get("David", 0)

# Or check first
if "David" in grades:
    score = grades["David"]
```

### ❌ Modifying Dictionary While Iterating
```python
# Wrong - can cause errors
for key in my_dict:
    if some_condition:
        del my_dict[key]

# Correct - iterate over copy
for key in list(my_dict.keys()):
    if some_condition:
        del my_dict[key]
```

### ❌ Using Mutable Keys
```python
# Wrong - lists can't be keys
my_dict = {[1, 2]: "value"}  # TypeError

# Correct - use tuples (immutable)
my_dict = {(1, 2): "value"}  # ✅
```

---

## Best Practices

✅ **Do**:
- Use descriptive key names
- Use `.get()` to avoid KeyErrors
- Check if key exists before accessing
- Use meaningful variable names for keys/values in loops

```python
# Good
for student_name, grades in class_grades.items():
    print(f"{student_name}: {grades}")

# Less clear
for k, v in d.items():
    print(f"{k}: {v}")
```

❌ **Avoid**:
- Overly nested structures (hard to read/maintain)
- Using dictionaries when lists would be simpler
- Mutating dictionaries during iteration

---

## Learning Resources

- [Python Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Dictionary Methods](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Nested Data Structures](https://realpython.com/python-nested-dictionary/)
- [max() and min() with key parameter](https://docs.python.org/3/library/functions.html#max)

---

## Real-World Applications

Dictionaries are everywhere in programming:

- **Configuration Files**: JSON, YAML → Python dicts
- **APIs**: REST responses are often JSON (dictionaries)
- **Caching**: Store computed results with keys
- **Counting**: Word frequency, vote tallies
- **Lookup Tables**: Translations, mappings
- **Database Records**: Represent rows as dictionaries
- **Game State**: Player stats, inventory, settings

---

## Fun Facts

- Python dictionaries are implemented as hash tables
- Dictionary lookup is O(1) average case - incredibly fast!
- Before Python 3.7, dictionaries didn't maintain insertion order
- The word "dictionary" comes from Latin "dictionarium" (collection of words)
- In other languages, dictionaries are called: maps, hash maps, associative arrays

---

## Quick Reference

```python
# Create
d = {}
d = {"key": "value"}

# Access
d["key"]           # Raises KeyError if missing
d.get("key")       # Returns None if missing
d.get("key", 0)    # Returns 0 if missing

# Add/Update
d["new_key"] = "value"

# Remove
del d["key"]
value = d.pop("key")
d.clear()  # Remove all

# Check existence
"key" in d         # True/False

# Methods
d.keys()           # All keys
d.values()         # All values
d.items()          # All key-value pairs

# Find max/min
max(d, key=d.get)  # Key with max value
max(d.values())    # Max value
```
