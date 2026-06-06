"""
Day 34 - Question Model

Represents a single trivia question.
"""


class Question:
    """Model for a trivia question with text and correct answer."""
    
    def __init__(self, text: str, answer: str):
        """Initialize a Question.
        
        Args:
            text: The question text
            answer: The correct answer (e.g., "True" or "False")
        """
        self.text = text
        self.answer = answer
    
    def __repr__(self):
        return f"Question(text='{self.text[:50]}...', answer='{self.answer}')"
