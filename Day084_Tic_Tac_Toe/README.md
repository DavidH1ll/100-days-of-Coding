# Day 84 - Tic Tac Toe

## Overview
A text-based Tic Tac Toe game playable in the command line. Features two-player mode, an unbeatable AI opponent using the minimax algorithm, colored X/O markers, score tracking, and a replay loop.

## Features

- **Two-Player Mode**: Local multiplayer with alternating X and O turns
- **AI Opponent**: Unbeatable minimax-based computer player — it will never lose
- **Colored Display**: Cyan X markers and yellow O markers for visual clarity
- **Reference Board**: Position numbers shown alongside the game board on each turn
- **Input Validation**: Rejects invalid positions, taken spots, and non-numeric input
- **Score Tracking**: Running tally of Player X wins, Player O wins, and draws
- **Replay Loop**: Play again without restarting, scores persist across games
- **Quit Anytime**: Type `q` during any move prompt to exit gracefully
- **Cross-Platform**: `clear_screen()` works on Windows, Linux, and macOS

## Usage

```bash
python Day084/tic_tac_toe.py
```

### Example Session

```
 _______ _        _______           _______
|__   __(_)      |__   __|         |__   __|
   | |   _  ___     | | __ _  ___     | | ___   ___
   | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \
   | |  | | (__     | | (_| | (__     | | (_) |  __/
   |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___|

Welcome to Tic Tac Toe!

Choose a game mode:
  1. Two Players
  2. Play vs AI
  3. Quit

Enter your choice (1/2/3): 2

Choose your symbol (X goes first): X
You are 'X'. The AI is 'O'.

   Your turn (X)

 X |   |
-----------
   |   |
-----------
   |   |

   Reference:
 1 | 2 | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9

Player X, choose a position (1-9): 5
```

### Board Display

```
 X | O | X       <-- Colored: X = cyan, O = yellow
-----------
 O | X |
-----------
   |   | O
```

## How It Works

### Board Representation
A 9-element list where index 0 = top-left, index 8 = bottom-right. Each cell is `'X'`, `'O'`, or `' '` (empty).

### Win Detection
Eight winning combinations checked after every move — 3 rows, 3 columns, 2 diagonals. Returns the winning player and the winning cells.

### AI Algorithm (Minimax)
- Recursively explores all possible future game states
- Assigns scores: +1 for AI win, -1 for human win, 0 for draw
- AI maximizes its score; simulates the human minimizing it
- On an empty board, picks a random corner or center (avoids always playing the same first move)
- Guarantees at least a draw — the AI cannot be beaten

## Key Concepts

- **Game Loop Architecture**: Flag-driven inner loop with outer replay/menu loop
- **Minimax Algorithm**: Recursive tree search with alternating maximizing/minimizing players
- **List State Management**: In-place board mutation with undo for tree exploration
- **Input Validation**: Multi-layer checks (type, range, availability, quit command)
- **ANSI Color Codes**: Terminal-colored output for X and O markers
- **Set Operations**: `get_available_moves()` for clean move enumeration

## Reflection

### How I Approached the Project

I started by studying the Day 11 Blackjack game to match the repo's game loop conventions — the flag-driven inner loop, the outer replay loop, the `clear_screen()` helper, and the `if __name__ == "__main__"` guard. I built the core game logic first (board display, move input, win detection) and tested it with assertions before adding the menu and AI.

For the AI, I considered three approaches: random moves, a heuristic-based player (block wins, take center), and minimax. I chose minimax because Tic Tac Toe's state space is tiny (9! = 362,880 possible game sequences, and with pruning far fewer) — the recursion completes instantly, so there's no performance downside to the "perfect" algorithm.

### What Was Hard

**Getting the AI to feel human-like on the first move.** The pure minimax algorithm always picks the same optimal first move (a corner). This makes the AI predictable and robotic. I solved it by special-casing the opening move: if the board is empty, pick randomly from corners and center. Small touch, but it makes the game feel less mechanical.

**The quit-during-input problem.** Players should be able to quit at any prompt, but `input()` blocks until they press Enter. I handled this by checking for `'q'` as a special input string and also catching `EOFError`/`KeyboardInterrupt` for Ctrl+D/Ctrl+C. It's not a true interrupt-based quit, but it's the best you can do with blocking `input()`.

**Display formatting.** Getting the board to look clean with the reference numbers below it, the logo above it, and the scoreboard after each game required careful placement of `clear_screen()` calls. Too many clears and the transition feels jarring; too few and old state bleeds into new screens. I settled on clearing before each turn and at game conclusion.

### What Was Easy

**Win detection** is just 8 hardcoded triplets — no clever algorithm needed. **Input validation** is a standard `while True` + `try/except` loop that I've written many times in this repo. The **ANSI color codes** (`\033[1;36m` for cyan X, `\033[1;33m` for yellow O) took one search query and worked first try.

### Biggest Learning

The minimax algorithm clicked for me in a way it hadn't before. The key insight: it's not just "AI picks the best move" — it's "AI assumes the human will also play optimally, so it evaluates every branch under that assumption." The recursion alternates between maximizing and minimizing, which mirrors the turn-taking structure of the game perfectly. Understanding *why* it works (not just *that* it works) was the real win.

### What I'd Do Differently

1. **Add alpha-beta pruning.** Pure minimax explores every node. Alpha-beta pruning would cut the search tree roughly in half — unnecessary for Tic Tac Toe but good practice for larger games like Connect Four.
2. **Add difficulty levels.** An "easy" AI that makes random moves 30% of the time, a "medium" AI that sometimes misses blocks, and the current "hard" unbeatable AI. This would make the single-player mode more accessible.
3. **Add a board animation for the AI's move.** Even a 0.3-second delay before the AI places its mark would make it feel like it's "thinking" rather than responding instantly.
4. **Save game history** to a file so players can review past matches and stats across sessions.
5. **Add a replay viewer** that steps through a completed game move-by-move — useful for learning from losses against the AI.

---

**Day 84: Complete!** ✅
