import os
import random
from time import sleep

def clear_screen():
    os.system('cls')

# ASCII art for cards and logo with fixed escape sequences
logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \\/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \\  /|K /\\  |     | '_ \\| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \\/ | /  \\ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \\  / |     |_.__/|_|\\__,_|\\___|_|\\_\\ |\\__,_|\\___|_|\\_\\
      |  \\/ K|                            _/ |                
      `------'                           |__/           
"""

def deal_card():
    """Return a random card from the deck."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Calculate score of a hand, handling aces."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack
    
    # Handle aces
    while 11 in cards and sum(cards) > 21:
        cards[cards.index(11)] = 1
        
    return sum(cards)

def play_game():
    clear_screen()
    print(logo)
    
    # Initial setup
    user_cards = []
    dealer_cards = []
    game_over = False
    
    # Initial deal
    for _ in range(2):
        user_cards.append(deal_card())
        dealer_cards.append(deal_card())
    
    while not game_over:
        user_score = calculate_score(user_cards)
        dealer_score = calculate_score(dealer_cards)
        
        print(f"\nYour cards: {user_cards}, current score: {user_score}")
        print(f"Dealer's first card: {dealer_cards[0]}")
        
        if user_score == 0 or dealer_score == 0 or user_score > 21:
            game_over = True
        else:
            should_continue = input("\nType 'y' to get another card, 'n' to pass: ").lower()
            if should_continue == 'y':
                user_cards.append(deal_card())
            else:
                game_over = True
    
    # Dealer's turn
    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)
    
    print(f"\nYour final hand: {user_cards}, final score: {user_score}")
    print(f"Dealer's final hand: {dealer_cards}, final score: {dealer_score}")
    print(determine_winner(user_score, dealer_score))

def determine_winner(user_score, dealer_score):
    if user_score > 21:
        return "You went over. You lose 😭"
    elif dealer_score > 21:
        return "Dealer went yover. You win 😃"
    elif user_score == dealer_score:
        return "Draw 🙃"
    elif user_score == 0:
        return "Win with a Blackjack 😎"
    elif dealer_score == 0:
        return "Lose, dealer has Blackjack 😱"
    elif user_score > dealer_score:
        return "You win 😃"
    else:
        return "You lose 😤"

while input("\nDo you want to play a game of Blackjack? Type 'y' or 'n': ").lower() == 'y':
    clear_screen()
    play_game()