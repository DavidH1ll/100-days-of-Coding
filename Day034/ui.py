"""
Day 34 - Quizzler UI

Tkinter-based GUI for the quiz application.
"""

import tkinter as tk
from quiz_brain import QuizBrain
from typing import Optional

THEME_COLOR = "#375362"
FONT_QUESTION = ("Arial", 20, "italic")
FONT_SCORE = ("Arial", 12, "bold")


class QuizInterface:
    """Graphical user interface for the quiz."""
    
    def __init__(self, quiz_brain: QuizBrain):
        """Initialize the UI with a QuizBrain instance.
        
        Args:
            quiz_brain: The QuizBrain managing quiz logic
        """
        self.quiz = quiz_brain
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        
        # Score label
        self.score_label = tk.Label(
            text="Score: 0",
            fg="white",
            bg=THEME_COLOR,
            font=FONT_SCORE
        )
        self.score_label.grid(row=0, column=1, pady=(0, 20))
        
        # Question canvas
        self.canvas = tk.Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Question will appear here",
            fill=THEME_COLOR,
            font=FONT_QUESTION
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # True button
        self.true_button = tk.Button(
            text="True",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=10,
            command=self.true_pressed,
            highlightthickness=0,
            relief="raised",
            bd=3
        )
        self.true_button.grid(row=2, column=0, padx=(0, 10))
        
        # False button
        self.false_button = tk.Button(
            text="False",
            font=("Arial", 14, "bold"),
            bg="#f44336",
            fg="white",
            width=10,
            command=self.false_pressed,
            highlightthickness=0,
            relief="raised",
            bd=3
        )
        self.false_button.grid(row=2, column=1, padx=(10, 0))
        
        self.get_next_question()
        
        self.window.mainloop()
    
    def get_next_question(self):
        """Display the next question or show final score."""
        self.canvas.config(bg="white")
        
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"You've completed the quiz!\n\nFinal Score: {self.quiz.score}/{self.quiz.question_number}"
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
    
    def true_pressed(self):
        """Handle True button click."""
        self.give_feedback(self.quiz.check_answer("True"))
    
    def false_pressed(self):
        """Handle False button click."""
        self.give_feedback(self.quiz.check_answer("False"))
    
    def give_feedback(self, is_correct: bool):
        """Provide visual feedback for answer correctness.
        
        Args:
            is_correct: Whether the answer was correct
        """
        if is_correct:
            self.canvas.config(bg="#90EE90")  # Light green
        else:
            self.canvas.config(bg="#FFB6C1")  # Light red
        
        # Disable buttons temporarily
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        
        # Schedule next question after delay
        self.window.after(1000, self.reset_and_next)
    
    def reset_and_next(self):
        """Re-enable buttons and move to next question."""
        self.true_button.config(state="normal")
        self.false_button.config(state="normal")
        self.get_next_question()
