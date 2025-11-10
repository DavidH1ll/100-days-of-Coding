"""
Day 34 - Quizzler App Entry Point

A quiz application using the Open Trivia Database API and tkinter GUI.
Displays true/false questions and tracks the user's score.
"""

from data import fetch_questions
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface


def main():
    """Initialize and run the Quizzler application."""
    
    # Fetch questions from API
    print("Fetching trivia questions...")
    question_data = fetch_questions(
        amount=10,
        category=None,  # Random categories (or use specific like 18 for Computers)
        difficulty=None,  # Random difficulty (or use "easy", "medium", "hard")
        question_type="boolean"
    )
    
    if not question_data:
        print("[ERROR] Could not fetch questions. Please check your internet connection.")
        return
    
    # Create Question objects
    question_bank = [
        Question(q["question"], q["correct_answer"]) 
        for q in question_data
    ]
    
    print(f"Loaded {len(question_bank)} questions. Starting quiz...\n")
    
    # Initialize quiz brain
    quiz = QuizBrain(question_bank)
    
    # Launch GUI
    quiz_ui = QuizInterface(quiz)


if __name__ == "__main__":
    main()
