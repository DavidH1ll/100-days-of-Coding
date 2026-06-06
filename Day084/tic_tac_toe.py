import os
import random

LOGO = r'''
 _______ _        _______           _______
|__   __(_)      |__   __|         |__   __|
   | |   _  ___     | | __ _  ___     | | ___   ___
   | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \
   | |  | | (__     | | (_| | (__     | | (_) |  __/
   |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___|

'''

BOARD_TEMPLATE = '''
 {0} | {1} | {2}
-----------
 {3} | {4} | {5}
-----------
 {6} | {7} | {8}
'''

WINNING_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

PLAYER_SYMBOLS = {'X': 'X', 'O': 'O'}
EMPTY = ' '


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_board(board, show_numbers=False):
    if show_numbers:
        cells = [str(i + 1) for i in range(9)]
    else:
        cells = []
        for i in range(9):
            if board[i] == EMPTY:
                cells.append(' ')
            else:
                cells.append(f'\033[1;36m{board[i]}\033[0m' if board[i] == 'X' else f'\033[1;33m{board[i]}\033[0m')
    print(BOARD_TEMPLATE.format(*cells))


def check_winner(board):
    for combo in WINNING_COMBOS:
        a, b, c = combo
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a], combo
    return None, None


def is_board_full(board):
    return EMPTY not in board


def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def get_player_move(board, player):
    while True:
        try:
            move = input(f"\nPlayer {player}, choose a position (1-9): ").strip()
            if move.lower() == 'q':
                return 'quit'
            position = int(move) - 1
            if position < 0 or position > 8:
                print("Invalid position. Please enter a number from 1 to 9.")
                continue
            if board[position] != EMPTY:
                print("That position is already taken. Choose another.")
                continue
            return position
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 9.")
        except (EOFError, KeyboardInterrupt):
            return 'quit'


def minimax(board, is_maximizing, ai_player, human_player):
    winner, _ = check_winner(board)
    if winner == ai_player:
        return 1
    if winner == human_player:
        return -1
    if is_board_full(board):
        return 0

    available = get_available_moves(board)

    if is_maximizing:
        best_score = -float('inf')
        for move in available:
            board[move] = ai_player
            score = minimax(board, False, ai_player, human_player)
            board[move] = EMPTY
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in available:
            board[move] = human_player
            score = minimax(board, True, ai_player, human_player)
            board[move] = EMPTY
            best_score = min(best_score, score)
        return best_score


def get_ai_move(board, ai_player, human_player):
    available = get_available_moves(board)

    if len(available) == 9:
        return random.choice([0, 2, 4, 6, 8])

    best_score = -float('inf')
    best_move = available[0]

    for move in available:
        board[move] = ai_player
        score = minimax(board, False, ai_player, human_player)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def play_two_player():
    board = [EMPTY] * 9
    current_player = 'X'

    while True:
        clear_screen()
        print(LOGO)
        print(f"   Player {current_player}'s turn\n")
        display_board(board)
        print("\n   Reference:")
        display_board(board, show_numbers=True)

        move = get_player_move(board, current_player)
        if move == 'quit':
            return None

        board[move] = current_player

        winner, winning_combo = check_winner(board)
        if winner:
            clear_screen()
            print(LOGO)
            display_board(board)
            print(f"\n🎉 Player {winner} wins!")
            return winner

        if is_board_full(board):
            clear_screen()
            print(LOGO)
            display_board(board)
            print("\n🤝 It's a draw!")
            return None

        current_player = 'O' if current_player == 'X' else 'X'


def play_vs_ai(player_choice):
    board = [EMPTY] * 9
    human_player = player_choice.upper()
    ai_player = 'O' if human_player == 'X' else 'X'
    current_player = 'X'

    print(f"\nYou are '{human_player}'. The AI is '{ai_player}'.")
    input("Press Enter to start...")

    while True:
        clear_screen()
        print(LOGO)

        if current_player == human_player:
            print(f"   Your turn ({human_player})\n")
        else:
            print(f"   AI is thinking ({ai_player})...\n")

        display_board(board)

        if current_player == human_player:
            print("\n   Reference:")
            display_board(board, show_numbers=True)
            move = get_player_move(board, current_player)
            if move == 'quit':
                return None
        else:
            move = get_ai_move(board, ai_player, human_player)

        board[move] = current_player

        winner, winning_combo = check_winner(board)
        if winner:
            clear_screen()
            print(LOGO)
            display_board(board)
            if winner == human_player:
                print("\n🎉 You win! The AI bows to you.")
            else:
                print("\n🤖 The AI wins! Better luck next time.")
            return winner

        if is_board_full(board):
            clear_screen()
            print(LOGO)
            display_board(board)
            print("\n🤝 It's a draw!")
            return None

        current_player = 'O' if current_player == 'X' else 'X'


def tic_tac_toe():
    scores = {'X': 0, 'O': 0, 'draws': 0}
    mode = None

    while True:
        clear_screen()
        print(LOGO)
        print("Welcome to Tic Tac Toe!\n")
        print("Choose a game mode:")
        print("  1. Two Players")
        print("  2. Play vs AI")
        print("  3. Quit")

        try:
            choice = input("\nEnter your choice (1/2/3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if choice == '1':
            mode = '2p'
        elif choice == '2':
            while True:
                try:
                    symbol = input("\nChoose your symbol (X goes first): ").strip().upper()
                    if symbol in ('X', 'O'):
                        break
                    print("Please choose X or O.")
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    return
            mode = 'ai'
        elif choice == '3':
            print("\nThanks for playing!")
            break
        else:
            print("\nInvalid choice. Press Enter to try again.")
            input()
            continue

        while True:
            if mode == '2p':
                winner = play_two_player()
            else:
                winner = play_vs_ai(symbol)

            if winner:
                scores[winner] += 1
            elif winner is None and mode:
                scores['draws'] += 1

            clear_screen()
            print(LOGO)
            print(f"   Scoreboard")
            print(f"   ----------")
            print(f"   Player X: {scores['X']}")
            print(f"   Player O: {scores['O']}")
            print(f"   Draws:    {scores['draws']}")

            try:
                again = input("\nPlay again? (y/n): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return

            if again != 'y':
                break


if __name__ == "__main__":
    try:
        tic_tac_toe()
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
