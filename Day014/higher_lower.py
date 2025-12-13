import random
import os
from time import sleep

def clear_screen():
    os.system('cls')

# ASCII art with fixed escape sequences
logo = """
    __  ___       __             
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \\/ _ \\/ ___/
 / __  / / /_/ / / / /  __/ /    
/_/ ///_/\\__, /_/ /_/\\___/_/     
   / /  /____/_      _____  _____
  / /   / __ \\ | /| / / _ \\/ ___/
 / /___/ /_/ / |/ |/ /  __/ /    
/_____/\\____/|__/|__/\\___/_/     
"""

vs = """
 _    __    
| |  / /____
| | / / ___/
| |/ (__  ) 
|___/____(_)
"""

# Game data dictionary
data = [
{
    'name': 'Ariana Grande',
    'follower_count': 183,
    'description': 'Musician and actress',
    'country': 'United States'
},
{
    'name': 'Dwayne Johnson',
    'follower_count': 181,
    'description': 'Actor and professional wrestler',
    'country': 'United States'
},
{
    'name': 'Selena Gomez',
    'follower_count': 174,
    'description': 'Musician and actress',
    'country': 'United States'
},
{
    'name': 'Kylie Jenner',
    'follower_count': 172,
    'description': 'Reality TV personality and businesswoman and Self-Made Billionaire',
    'country': 'United States'
},
{
    'name': 'Kim Kardashian',
    'follower_count': 167,
    'description': 'Reality TV personality and businesswoman',
    'country': 'United States'
},
{
    'name': 'Lionel Messi',
    'follower_count': 149,
    'description': 'Footballer',
    'country': 'Argentina'
},
{
    'name': 'Beyoncé',
    'follower_count': 145,
    'description': 'Musician',
    'country': 'United States'
},
{
    'name': 'Neymar',
    'follower_count': 138,
    'description': 'Footballer',
    'country': 'Brazil'
},
{
    'name': 'National Geographic',
    'follower_count': 135,
    'description': 'Magazine',
    'country': 'United States'
},
{
    'name': 'Justin Bieber',
    'follower_count': 133,
    'description': 'Musician',
    'country': 'Canada'
}
]

def format_data(account):
    """Format account data into printable format."""
    return f"{account['name']}, a {account['description']}, from {account['country']}"

def check_answer(guess, a_followers, b_followers):
    """Check if user's guess is correct."""
    if a_followers > b_followers:
        return guess == 'a'
    else:
        return guess == 'b'

def play_game():
    clear_screen()
    score = 0
    game_should_continue = True
    account_b = random.choice(data)

    while game_should_continue:
        account_a = account_b
        account_b = random.choice(data)
        while account_a == account_b:
            account_b = random.choice(data)

        clear_screen()
        print(logo)
        if score > 0:
            print(f"You're right! Current score: {score}")
        
        print(f"Compare A: {format_data(account_a)}")
        print(vs)
        print(f"Against B: {format_data(account_b)}")
        
        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        
        a_follower_count = account_a['follower_count']
        b_follower_count = account_b['follower_count']
        is_correct = check_answer(guess, a_follower_count, b_follower_count)
        
        clear_screen()
        print(logo)
        
        if is_correct:
            score += 1
            print(f"You're right! Current score: {score}")
            sleep(1)
        else:
            print(f"Sorry, that's wrong. Final score: {score}")
            game_should_continue = False

if __name__ == "__main__":
    while input("\nDo you want to play Higher Lower? (y/n): ").lower() == 'y':
        play_game()