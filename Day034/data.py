"""
Day 34 - Quizzler Data Module

Fetches trivia questions from Open Trivia Database API.
"""

import html
import requests
from typing import List, Dict, Optional


TRIVIA_API_URL = "https://opentdb.com/api.php"


def fetch_questions(
    amount: int = 10,
    category: Optional[int] = None,
    difficulty: Optional[str] = None,
    question_type: str = "boolean"
) -> List[Dict[str, str]]:
    """Fetch trivia questions from Open Trivia Database.
    
    Args:
        amount: Number of questions (1-50)
        category: Category ID (e.g., 9=General Knowledge, 18=Science: Computers)
        difficulty: "easy", "medium", or "hard"
        question_type: "boolean" for True/False, "multiple" for multiple choice
    
    Returns:
        List of question dictionaries with keys: 'question', 'correct_answer'
    """
    params = {
        "amount": amount,
        "type": question_type
    }
    
    if category is not None:
        params["category"] = category
    
    if difficulty is not None:
        params["difficulty"] = difficulty
    
    try:
        response = requests.get(TRIVIA_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("response_code") != 0:
            print(f"[WARN] API returned code {data.get('response_code')}")
            return []
        
        # Decode HTML entities in questions and answers
        questions = []
        for item in data.get("results", []):
            questions.append({
                "question": html.unescape(item["question"]),
                "correct_answer": html.unescape(item["correct_answer"])
            })
        
        return questions
    
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch questions: {e}")
        return []


if __name__ == "__main__":
    # Test the API
    test_questions = fetch_questions(amount=5)
    for i, q in enumerate(test_questions, 1):
        print(f"{i}. {q['question']}")
        print(f"   Answer: {q['correct_answer']}\n")
