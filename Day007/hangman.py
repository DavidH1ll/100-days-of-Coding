import os
import random
import string

# Hangman visual states with fixed escape sequences
HANGMAN_STAGES = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========''']

# Word bank
words = ['python', 'programming', 'computer', 'algorithm', 'database', 
         'network', 'software', 'developer', 'internet', 'javascript']

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_hangman():
    word = random.choice(words).lower()
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_lowercase)
    used_letters = set()  # letters guessed by user
    
    lives = 6
    
    # Game loop
    while len(word_letters) > 0 and lives > 0:
        clear_screen()  # Clear screen before each update
        print(f"\nYou have {lives} lives left.")
        print("Used letters:", " ".join(used_letters))
        
        # Show current word state
        word_list = [letter if letter in used_letters else "_" for letter in word]
        print(HANGMAN_STAGES[6 - lives])
        print("Current word:", " ".join(word_list))
        
        # Get user input
        guess = input("Guess a letter: ").lower()
        if guess in alphabet - used_letters:
            used_letters.add(guess)
            if guess in word_letters:
                word_letters.remove(guess)
            else:
                lives = lives - 1
                print(f"\nYour letter {guess} is not in the word.")
        
        elif guess in used_letters:
            print("\nYou've already used that letter. Please try again.")
        
        else:
            print("\nInvalid character. Please try again.")
    
    # Final screen
    clear_screen()
    if lives == 0:
        print(HANGMAN_STAGES[6])
        print(f"Sorry, you died. The word was {word}")
    else:
        print(f"Congratulations! You guessed the word {word}!!")

if __name__ == "__main__":
    print("Welcome to Hangman!")
    play_hangman()