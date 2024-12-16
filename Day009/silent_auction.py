import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

logo = '''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''

def format_winner_banner(winner_name):
    return f'''
╔══════════════════════════════════════════════════════════════╗
    🏆 {winner_name.upper()} IS THE WINNER! 🏆                
║                                                              ║
║                                                              ║
║   ██╗    ██╗██╗███╗   ██╗███╗   ██╗███████╗██████╗ ██╗       ║
║   ██║    ██║██║████╗  ██║████╗  ██║██╔════╝██╔══██╗██║       ║
║   ██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝██║       ║
║   ██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗╚═╝       ║
║   ╚███╔███╔╝██║██║ ╚████║██║ ╚████║███████╗██║  ██║██╗       ║
║    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
'''

def secret_auction():
    bids = {}
    bidding_finished = False
    
    # Clear screen and show initial display
    clear_screen()
    print(logo)
    print("Welcome to the Secret Auction Program!")
    
    while not bidding_finished:
        name = input("What is your name?: ")
        try:
            bid = float(input("What's your bid?: $"))
            bids[name] = bid
        except ValueError:
            print("Please enter a valid number!")
            continue
        
        should_continue = input("Are there any other bidders? (yes/no): ").lower()
        if should_continue != "yes":
            bidding_finished = True
        clear_screen()
        print(logo)
    
    # Find and display winner
    winner = max(bids, key=bids.get)
    winning_bid = bids[winner]
    
    clear_screen()
    print(format_winner_banner(winner))
    print(f"\nWinning bid: ${winning_bid:.2f}!")

if __name__ == "__main__":
    secret_auction()