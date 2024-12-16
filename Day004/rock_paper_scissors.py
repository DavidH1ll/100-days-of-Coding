import random

# ASCII art for game choices
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

try:
    # Get player choice
    print("Let's play Rock, Paper, Scissors!")
    print("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.")
    
    player_choice = int(input())
    game_images = [rock, paper, scissors]
    
    if player_choice >= 3 or player_choice < 0:
        print("Invalid number! You lose!")
    else:
        print("\nYou chose:")
        print(game_images[player_choice])
        
        # Generate computer choice
        computer_choice = random.randint(0, 2)
        print("Computer chose:")
        print(game_images[computer_choice])
        
        # Determine winner
        if player_choice == computer_choice:
            print("It's a draw!")
        elif (player_choice == 0 and computer_choice == 2) or \
             (player_choice == 1 and computer_choice == 0) or \
             (player_choice == 2 and computer_choice == 1):
            print("You win!")
        else:
            print("You lose!")

except ValueError:
    print("Please enter a valid number!")
except Exception as e:
    print(f"An error occurred: {str(e)}")