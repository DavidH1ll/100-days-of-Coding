"""
Day 34 - Quiz Brain

Manages quiz logic: question iteration, answer checking, and scoring.
"""

from question_model import Question
from typing import List, Optional


class QuizBrain:
    """Controls quiz flow and tracks state."""
    
    def __init__(self, question_list: List[Question]):
        """Initialize quiz with a list of questions.
        
        Args:
            question_list: List of Question objects
        """
        self.question_number = 0
        self.score = 0
        self.question_list = question_list
        self.current_question: Optional[Question] = None
    
    def still_has_questions(self) -> bool:
        """Check if there are more questions remaining."""
        return self.question_number < len(self.question_list)
    
    def next_question(self) -> str:
        """Get the next question text.
        
        Returns:
            Formatted question string with question number
        """
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        return f"Q.{self.question_number}: {self.current_question.text}"
    
    def check_answer(self, user_answer: str) -> bool:
        """Check if the user's answer is correct.
        
        Args:
            user_answer: The user's answer string
        
        Returns:
            True if correct, False otherwise
        """
        correct_answer = self.current_question.answer
        is_correct = user_answer.lower() == correct_answer.lower()
        
        if is_correct:
            self.score += 1
        
        return is_correct
