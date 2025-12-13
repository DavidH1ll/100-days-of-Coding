import random
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls')

logo = """
 _____                    _____ _            _    _                 _               
|   __|_ _ ___ ___ ___   |_   _| |_ ___     | \\ | |_   _ _ __ ___ | |__   ___ _ __ 
|  |  | | | -_|_ -|_ -|    | | |   | -_|    |  \\| | | | | '_ ` _ \\| '_ \\ / _ \\ '__|
|_____|___|___|___|___|    |_| |_|_|___|    | |\\  | |_| | | | | | | |_) |  __/ |   
                                            |_| \\_|\\__,_|_| |_| |_|_.__/ \\___|_|
"""

def game():
    clear_screen()
    print(logo)
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Generate answer
    answer = random.randint(1, 100)
    
    # Set difficulty
    while True:
        difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
        if difficulty in ['easy', 'hard']:
            break
        print("Invalid input. Please type 'easy' or 'hard'.")
    
    attempts = 10 if difficulty == "easy" else 5
    
    # Game loop
    while attempts > 0:
        print(f"\nYou have {attempts} attempts remaining.")
        
        # Get and validate guess
        try:
            guess = int(input("Make a guess: "))
            if guess < 1 or guess > 100:
                print("Please guess a number between 1 and 100.")
                continue
                
            if guess == answer:
                print(f"\nYou got it! The answer was {answer}")
                return
            elif guess > answer:
                print("Too high.")
            else:
                print("Too low.")
            
            attempts -= 1
            if attempts == 0:
                print(f"\nGame Over. The answer was {answer}")
                
        except ValueError:
            print("Please enter a valid number!")

if __name__ == "__main__":
    while input("\nDo you want to play? (y/n): ").lower() == 'y':
        game()