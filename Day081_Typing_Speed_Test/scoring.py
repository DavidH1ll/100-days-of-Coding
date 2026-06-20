"""Pure scoring functions and passage data for the typing speed test.

Separated from the tkinter GUI in ``main.py`` so the math can be unit
tested without a display.
"""

from __future__ import annotations

PASSAGES: list[str] = [
    "The quick brown fox jumps over the lazy dog near the river bank yesterday afternoon while children played in the park.",
    "Programming is the art of telling another human what one wants the computer to do by writing instructions in a language both can understand.",
    "Python is an interpreted high-level general-purpose programming language known for its readability and versatility across many domains from web to data science.",
    "The best way to predict the future is to invent it by taking action today rather than waiting for circumstances to change on their own.",
    "Learning to code is like learning a new language it takes practice patience and persistence but the rewards are well worth the effort.",
    "Software engineering is not just about writing code it is about solving problems and building systems that make peoples lives better.",
    "The journey of a thousand miles begins with a single step and every expert was once a beginner who refused to give up on their dreams.",
    "Technology is best when it brings people together and creates opportunities that did not exist before the digital revolution began.",
    "Success is not final failure is not fatal it is the courage to continue that counts and determines how far you will go in life.",
    "The only way to do great work is to love what you do and never settle for anything less than your best effort in everything you attempt.",
    "Innovation distinguishes between a leader and a follower and those who dare to think differently are the ones who change the world around them.",
    "Debugging is twice as hard as writing the code in the first place therefore if you write the code as cleverly as possible you are by definition not smart enough to debug it.",
    "First solve the problem then write the code and always remember that readability counts more than cleverness in production software.",
    "Algorithms are the computational building blocks of computer science and understanding them deeply separates good programmers from great ones.",
    "Data structures and algorithms form the foundation of efficient programming and are essential knowledge for any serious software developer.",
]

CHARS_PER_WORD = 5
MIN_MINUTES = 0.01


def compute_wpm(correct_chars: int, elapsed_seconds: float) -> int:
    """Compute words-per-minute from correctly-typed characters and elapsed seconds.

    Uses a 5-character average word length. The result is floored to an
    integer (the GUI shows whole WPM values).

    Args:
        correct_chars: Number of characters typed that matched the passage.
        elapsed_seconds: Total elapsed time in seconds.

    Returns:
        Words per minute as an integer.
    """
    minutes = max(elapsed_seconds / 60, MIN_MINUTES)
    return int((correct_chars / CHARS_PER_WORD) / minutes)


def compute_accuracy(correct_chars: int, total_chars: int) -> int:
    """Compute accuracy as an integer percentage (0-100).

    Returns 0 if no characters have been typed, to avoid division by zero.
    """
    if total_chars <= 0:
        return 0
    return int(correct_chars / total_chars * 100)


def compute_completion(typed_chars: int, total_chars: int) -> int:
    """Compute completion as an integer percentage (0-100), capped at 100.

    Useful when the user types more than the passage length (we cap at
    100% rather than overflow).
    """
    if total_chars <= 0:
        return 0
    return int(min(typed_chars, total_chars) / total_chars * 100)
