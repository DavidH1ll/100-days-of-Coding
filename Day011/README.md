# Day 11 - Blackjack (Capstone Project)

## Overview
Day 11 is the first capstone project, bringing together all concepts learned in Days 1-10 to build a complete Blackjack card game. This project demonstrates game logic, score calculation, AI opponent behavior, and user interaction in a real-world application.

## Project: Blackjack Game (`blackjack.py`)

A fully functional implementation of the classic casino card game.

### Features

✅ **Complete Blackjack Rules**: Follows standard casino rules  
✅ **Ace Handling**: Aces count as 11 or 1 automatically  
✅ **Blackjack Detection**: Natural 21 with 2 cards  
✅ **Dealer AI**: Dealer hits until reaching 17  
✅ **Multiple Rounds**: Play as many games as you want  
✅ **ASCII Art**: Stylish game logo  
✅ **Win Detection**: All win/lose/draw conditions  
✅ **Clean Interface**: Screen clearing between games  

### Blackjack Rules

#### Objective
Get as close to 21 as possible without going over (bust).

#### Card Values
- **Number cards**: Face value (2-10)
- **Face cards** (J, Q, K): Worth 10
- **Ace**: Worth 11 or 1 (automatically adjusted)

#### Gameplay
1. **Initial Deal**: Player and dealer each get 2 cards
2. **Player's Turn**: 
   - See your cards and one dealer card
   - Choose to "hit" (take card) or "stand" (keep current hand)
   - Can hit multiple times
   - Bust if over 21
3. **Dealer's Turn**:
   - Reveals hidden card
   - Must hit until reaching 17 or higher
   - Dealer busts if over 21

#### Winning Conditions
- **Blackjack**: Natural 21 with 2 cards (Ace + 10-value card)
- **Higher Score**: Closer to 21 than dealer without busting
- **Dealer Bust**: Dealer goes over 21
- **Draw**: Same score as dealer

### Usage

```powershell
python blackjack.py
```

### Example Game Session

```
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
      |  \/ K|                            _/ |                
      `------'                           |__/           

Do you want to play a game of Blackjack? Type 'y' or 'n': y

Your cards: [10, 11], current score: 21
Dealer's first card: 7

Your final hand: [10, 11], final score: 0
Dealer's final hand: [7, 8, 6], final score: 21
Win with a Blackjack 😎

Do you want to play a game of Blackjack? Type 'y' or 'n': y

Your cards: [5, 8], current score: 13
Dealer's first card: 10

Type 'y' to get another card, 'n' to pass: y

Your cards: [5, 8, 7], current score: 20
Dealer's first card: 10

Type 'y' to get another card, 'n' to pass: n

Your final hand: [5, 8, 7], final score: 20
Dealer's final hand: [10, 8], final score: 18
You win 😃
```

---

## Key Concepts Covered

### 1. Game State Management

```python
# Track game state with variables
user_cards = []
dealer_cards = []
game_over = False

# Update state throughout game
if user_score > 21:
    game_over = True
```

### 2. Random Card Selection

```python
def deal_card():
    """Return a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)
```

**Why multiple 10s?**: Represents 10, J, Q, K (4 cards worth 10)  
**Why 11 for Ace?**: Start as 11, convert to 1 if needed

### 3. Dynamic Ace Handling

```python
def calculate_score(cards):
    """Calculate score of a hand, handling aces."""
    # Detect blackjack (21 with 2 cards)
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Special value for blackjack
    
    # Convert Ace from 11 to 1 if busting
    while 11 in cards and sum(cards) > 21:
        cards[cards.index(11)] = 1
    
    return sum(cards)
```

**Why return 0 for Blackjack?**: Makes win/loss logic simpler

### 4. Game Loop Structure

```python
while not game_over:
    # 1. Calculate scores
    # 2. Display current state
    # 3. Check end conditions
    # 4. Get player decision
    # 5. Update game state
```

### 5. AI Dealer Logic

```python
# Dealer must hit until reaching 17
while dealer_score != 0 and dealer_score < 17:
    dealer_cards.append(deal_card())
    dealer_score = calculate_score(dealer_cards)
```

Standard casino rule: Dealer has no choice, must follow this pattern

### 6. Win Condition Logic

```python
def determine_winner(user_score, dealer_score):
    if user_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Dealer went over. You win 😃"
    elif user_score == dealer_score:
        return "Draw 🙃"
    elif user_score == 0:  # Blackjack
        return "Win with a Blackjack 😎"
    elif dealer_score == 0:  # Dealer blackjack
        return "Lose, dealer has Blackjack 😱"
    elif user_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"
```

**Priority order matters**:
1. Check for busts first
2. Check for draws
3. Check for blackjacks
4. Compare scores

### 7. Replay Mechanism

```python
while input("\nPlay again? Type 'y' or 'n': ").lower() == 'y':
    clear_screen()
    play_game()
```

---

## Code Structure

```
blackjack.py
├── Imports (os, random, time)
├── clear_screen() - Clear terminal
├── logo - ASCII art
├── deal_card() - Random card generation
├── calculate_score() - Score with ace handling
├── determine_winner() - Win/lose logic
├── play_game() - Main game loop
└── Main loop - Replay mechanism
```

---

## Running the Project

From the repository root:
```powershell
python .\Day011\blackjack.py
```

Or navigate to Day011:
```powershell
cd Day011
python blackjack.py
```

---

## Challenges & Extensions

### Easy
- Display card suits (♠ ♥ ♦ ♣)
- Add win/loss statistics tracking
- Show remaining cards in deck
- Add color to output (using `colorama`)
- Display card values as J, Q, K instead of 10

### Medium
- **Betting System**: Start with chips, bet on each hand
- **Multiple Decks**: Use 6-8 decks like real casinos
- **Split Pairs**: Split matching cards into two hands
- **Double Down**: Double bet for one more card
- **Insurance**: Bet on dealer blackjack when showing Ace
- **Surrender**: Give up half bet to fold early
- **Card Counting**: Show running count for practice
- **Save/Load Game**: Resume game later

### Advanced
- **Multiplayer**: Multiple players vs dealer
- **GUI Version**: Build with `tkinter` or `pygame`
- **Online Multiplayer**: Network play with sockets
- **AI Opponent**: Implement basic strategy
- **Deck Visualization**: Graphical cards
- **Tournament Mode**: Compete against AI players
- **Probability Calculator**: Show odds of busting
- **Perfect Strategy Hints**: Suggest optimal play
- **Casino Simulator**: Multiple tables, different rules

---

## Blackjack Strategy Tips

### Basic Strategy

**Player 12-16, Dealer 2-6**: Stand (dealer likely to bust)  
**Player 12-16, Dealer 7-Ace**: Hit (dealer likely strong)  
**Player 17+**: Always stand  
**Player 11 or less**: Always hit  
**Soft 17 (Ace-6)**: Hit  
**Soft 18+**: Stand  

### Card Counting Basics

**High-Low System**:
- Low cards (2-6): +1
- Neutral (7-9): 0
- High cards (10-Ace): -1

Positive count = more high cards remaining = player advantage

⚠️ **Note**: Card counting is legal but casinos don't like it!

---

## Common Mistakes & Solutions

### ❌ Not Handling Aces Properly
```python
# Wrong - fixed value
score = sum(cards)  # Aces always 11

# Correct - dynamic value
while 11 in cards and sum(cards) > 21:
    cards[cards.index(11)] = 1
```

### ❌ Dealer Playing Incorrectly
```python
# Wrong - dealer shouldn't make choices
if dealer_score < 17 or random.random() > 0.5:
    hit()

# Correct - dealer must follow rules
while dealer_score < 17:
    dealer_cards.append(deal_card())
```

### ❌ Wrong Win Detection Order
```python
# Wrong - checks score before bust
if user_score > dealer_score:
    return "Win"
elif user_score > 21:
    return "Bust"

# Correct - check bust first
if user_score > 21:
    return "Bust"
elif user_score > dealer_score:
    return "Win"
```

---

## Learning Outcomes

After completing Day 11, you should be able to:

✅ Combine multiple concepts into a cohesive program  
✅ Implement complex game logic with multiple conditions  
✅ Handle edge cases (aces, blackjack, bust)  
✅ Create AI opponent behavior  
✅ Manage game state throughout execution  
✅ Structure code with multiple functions  
✅ Test and debug complex logic  
✅ Create replay mechanisms  

---

## Concepts Review (Days 1-11)

This project uses everything learned so far:

- **Day 1**: Print statements, variables
- **Day 2**: Data types (int, float), type conversion
- **Day 3**: If/elif/else conditionals
- **Day 4**: Lists, random module
- **Day 5**: For loops, range()
- **Day 6**: While loops, functions
- **Day 7**: Combining concepts (Hangman)
- **Day 8**: Function parameters
- **Day 9**: Dictionaries (could use for cards)
- **Day 10**: Function returns
- **Day 11**: Integration of all above!

---

## Real-World Applications

Game development concepts used here apply to:

- **Video Games**: State management, game loops
- **Simulations**: Modeling real-world systems
- **AI Development**: Opponent behavior, decision trees
- **Mobile Apps**: Turn-based games
- **Web Games**: Browser-based card games
- **Probability Studies**: Monte Carlo simulations

---

## Learning Resources

- [Blackjack Rules](https://www.blackjackinfo.com/blackjack-rules/)
- [Basic Strategy](https://www.blackjackinfo.com/blackjack-basic-strategy-engine/)
- [Card Counting](https://www.blackjackinfo.com/card-counting/)
- [Python Game Development](https://realpython.com/pygame-a-primer/)
- [Random Module](https://docs.python.org/3/library/random.html)

---

## Fun Facts

- Blackjack originated in French casinos around 1700s as "Vingt-et-Un" (21)
- The name "Blackjack" comes from a special bonus for Ace of Spades + Jack of Spades
- With perfect strategy, house edge is only ~0.5%
- Card counting can give players a 1-2% edge over the casino
- MIT students won millions using card counting teams
- Online blackjack uses continuous shuffle machines (card counting impossible)
- Blackjack is the most popular casino card game worldwide

---

## Quick Reference

### Card Values
```python
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# 11 = Ace, 10 appears 4 times (10, J, Q, K)
```

### Blackjack Detection
```python
if sum(cards) == 21 and len(cards) == 2:
    # Blackjack!
```

### Ace Conversion
```python
while 11 in cards and sum(cards) > 21:
    cards[cards.index(11)] = 1
```

### Dealer Logic
```python
while dealer_score < 17:
    dealer_cards.append(deal_card())
```

---

Congratulations on completing your first capstone project! 🎉

This marks the end of the beginner section. You now have the foundation to build real programs!
