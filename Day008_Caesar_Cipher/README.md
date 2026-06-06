# Day 8 - Function Parameters & Caesar Cipher

## Overview
Day 8 deepens understanding of function parameters, arguments, and introduces cryptography with the classic Caesar Cipher. Learn about positional vs keyword arguments, parameter order, and practical applications of string manipulation.

## Projects

### 1. Function Parameters Practice (`exercises.py`)

Simple exercises demonstrating different ways to pass arguments to functions.

**Key Concepts**:
- Positional arguments (order matters)
- Keyword arguments (order doesn't matter)
- Default parameters

```python
def greet_with_location(name, location):
    print(f"Hello {name}")
    print(f"What is it like in {location}?")

# Positional arguments
greet_with_location("Angela", "London")

# Keyword arguments (can be in any order)
greet_with_location(location="London", name="Angela")
```

**Usage**:
```powershell
python exercises.py
```

---

### 2. Love Calculator (`loveCalculator.py`)

A fun program that calculates a "love score" between two names based on letter occurrences.

#### How It Works
1. Combines both names into a single string
2. Counts occurrences of letters in "TRUE"
3. Counts occurrences of letters in "LOVE"
4. Combines counts into a two-digit score

#### Example
```
Enter first name: Angela
Enter second name: Jack

The love score for Angela and Jack is: 42
```

**Calculation**:
- "ANGELAJ ACK" contains: T(0), R(0), U(0), E(1) → TRUE score = 1
- "ANGELAJ ACK" contains: L(1), O(0), V(0), E(1) → LOVE score = 2
- Combined: 12 (not 42 - example shows logic, not exact output)

**Key Concepts**:
- String concatenation
- `.upper()` method for case-insensitive counting
- `.count()` method for character counting
- String manipulation for number concatenation

**Usage**:
```powershell
python loveCalculator.py
```

---

### 3. Caesar Cipher (`ceasercypher.py`) 🔐

A complete encryption/decryption program using the Caesar Cipher algorithm.

#### What is Caesar Cipher?

A substitution cipher where each letter is shifted by a fixed number of positions in the alphabet. Used by Julius Caesar to protect military messages!

**Example** (shift of 3):
- Plain: `HELLO`
- Cipher: `KHOOR`

#### Features
✅ **Encode & Decode**: Encrypt or decrypt messages  
✅ **Custom Shift**: Choose any shift value  
✅ **Large Shifts**: Handles shifts > 26 with modulo  
✅ **Preserves Non-letters**: Spaces, punctuation unchanged  
✅ **Case Handling**: Converts to lowercase  
✅ **Screen Clearing**: Clean interface  
✅ **Error Handling**: Validates inputs  

#### Usage

```powershell
python ceasercypher.py
```

#### Example Session

**Encoding**:
```
Welcome to Caesar Cipher!
------------------------

Type 'encode' to encrypt, type 'decode' to decrypt:
> encode
Type your message:
> hello world
Type the shift number:
> 5

The encoded text is: mjqqt btwqi
```

**Decoding**:
```
Type 'encode' to encrypt, type 'decode' to decrypt:
> decode
Type your message:
> mjqqt btwqi
Type the shift number:
> 5

The decoded text is: hello world
```

#### How It Works

1. **Get Direction**: Encode or decode
2. **Get Message**: User's text (converted to lowercase)
3. **Get Shift**: Number of positions to shift
4. **Normalize Shift**: `shift % 26` handles shifts > 26
5. **Reverse for Decode**: Multiply shift by -1 if decoding
6. **Process Each Character**:
   - If letter: Find index, shift position, get new letter
   - If not letter: Keep unchanged
7. **Display Result**

#### Algorithm Breakdown

```python
alphabet = ['a', 'b', 'c', ..., 'z']

for char in text:
    if char in alphabet:
        position = alphabet.index(char)  # Find current position
        new_position = (position + shift) % 26  # Shift and wrap
        result += alphabet[new_position]
    else:
        result += char  # Keep spaces, punctuation, etc.
```

**Modulo Magic**: `% 26` ensures wrapping
- `(25 + 3) % 26 = 2` (z → c)
- `(0 - 5) % 26 = 21` (a → v when decoding)

---

## Key Concepts Covered

### 1. Function Parameters

#### Positional Arguments
Order matters!
```python
def greet(first_name, last_name):
    print(f"Hello {first_name} {last_name}")

greet("John", "Doe")  # Correct
greet("Doe", "John")  # Wrong order!
```

#### Keyword Arguments
Order doesn't matter!
```python
greet(last_name="Doe", first_name="John")  # Works!
```

#### Default Parameters
```python
def greet(name="stranger"):
    print(f"Hello {name}")

greet()           # Hello stranger
greet("Alice")    # Hello Alice
```

#### Mixing Positional & Keyword
```python
# Positional MUST come before keyword
greet("John", last_name="Doe")  # ✅ Valid
greet(first_name="John", "Doe")  # ❌ SyntaxError
```

### 2. String Methods

```python
text = "Hello World"

text.lower()         # "hello world"
text.upper()         # "HELLO WORLD"
text.count('l')      # 3
text.index('W')      # 6
text.replace('l', 'L')  # "HeLLo WorLd"
```

### 3. Modulo Operator for Wrapping

```python
# Wrap around in circular lists
alphabet_size = 26
position = 28  # Beyond alphabet

wrapped = position % 26  # 2 (wraps to 'c')
```

### 4. List Indexing

```python
alphabet = ['a', 'b', 'c', 'd']

alphabet[0]        # 'a'
alphabet.index('c')  # 2
alphabet[2]        # 'c'

# Negative indexing
alphabet[-1]       # 'd' (last element)
```

---

## Running the Projects

From the repository root:
```powershell
# Function parameters
python .\Day008\exercises.py

# Love calculator
python .\Day008\loveCalculator.py

# Caesar cipher
python .\Day008\ceasercypher.py
```

Or navigate to Day008:
```powershell
cd Day008
python exercises.py
python loveCalculator.py
python ceasercypher.py
```

---

## Challenges & Extensions

### Caesar Cipher Enhancements

**Easy**:
- Add a replay loop to encode/decode multiple messages
- Display the full alphabet with shift visualization
- Add input validation for shift range (1-25)
- Create a "Caesar cipher wheel" ASCII art

**Medium**:
- **Brute Force Decoder**: Try all 26 possible shifts
- **Frequency Analysis**: Show letter frequency distribution
- **File Support**: Encrypt/decrypt entire text files
- **Custom Alphabet**: Allow user-defined character sets
- **GUI Version**: Build with `tkinter`

**Advanced**:
- **Vigenère Cipher**: Use a keyword for shifting (stronger encryption)
- **ROT13**: Special case of Caesar (shift 13)
- **Rainbow Table**: Pre-compute common word transformations
- **Dictionary Attack**: Check if decoded text contains real words
- **Other Ciphers**: Implement Atbash, substitution, transposition ciphers

### Love Calculator Enhancements

- Add compatibility percentage
- Include zodiac sign compatibility
- Use date of birth for calculations
- Create a GUI with hearts and animations
- Store results in a file

---

## Cryptography Concepts

### Caesar Cipher History
- Used by Julius Caesar (~100 BCE)
- Originally used shift of 3
- One of the simplest encryption methods
- Easily broken with frequency analysis

### Cipher Strengths & Weaknesses

**Strengths**:
- ✅ Simple to implement
- ✅ Fast encryption/decryption
- ✅ No key management needed

**Weaknesses**:
- ❌ Only 25 possible keys (easy brute force)
- ❌ Letter frequency preserved
- ❌ Vulnerable to frequency analysis
- ❌ Not secure for modern use

### Breaking Caesar Cipher

**Method 1: Brute Force**
Try all 26 shifts (trivial with computers)

**Method 2: Frequency Analysis**
- 'E' is most common in English (~12.7%)
- Find most common letter in ciphertext
- Calculate shift from 'E'

**Method 3: Dictionary Attack**
- Try shifts until recognizable words appear
- Use word lists to validate decryption

---

## Learning Resources

- [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Function Arguments](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Caesar Cipher (Wikipedia)](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Cryptography Basics](https://www.khanacademy.org/computing/computer-science/cryptography)

---

## Security Note

⚠️ **Never use Caesar Cipher for real security!**

Modern encryption uses:
- AES (Advanced Encryption Standard)
- RSA (Rivest-Shamir-Adleman)
- ChaCha20
- Elliptic Curve Cryptography

For learning Python encryption:
- `cryptography` library
- `PyCrypto` / `PyCryptodome`

---

## Fun Facts

- ROT13 (shift 13) is its own inverse: encoding twice gives original text
- Caesar cipher is featured in many escape rooms and puzzles
- The Enigma machine (WWII) was essentially a complex rotating Caesar cipher
- Some modern systems still use simple ciphers for obfuscation (not security)
- Caesar cipher appears in many video games as puzzle mechanics

---

## Quick Reference

### Function Parameters
```python
# Positional
def func(a, b, c):
    pass
func(1, 2, 3)

# Keyword
func(c=3, a=1, b=2)

# Default
def func(a, b=10):
    pass
func(5)  # b defaults to 10

# Mixed
func(5, b=20)
```

### Caesar Cipher Formula
```
Encryption: E(x) = (x + shift) mod 26
Decryption: D(x) = (x - shift) mod 26
```

Where x is the letter's position (a=0, b=1, ..., z=25)
