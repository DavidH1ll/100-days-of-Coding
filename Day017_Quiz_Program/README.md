# Day 17 – Quiz Program (OOP Foundations)

## Goal
Apply object-oriented programming to build a reusable True/False quiz engine.

## Files
- data.py – question bank (list of dicts).
- question_model.py – `Question` class (text / answer).
- quiz_brain.py – `QuizBrain` class (state: question number, scoring, progression).
- examples.py – small OOP practice snippets.
- main.py – assembles questions, runs quiz loop.

## Concepts Practiced
- Classes and instances.
- Initialization (`__init__`), attributes, methods.
- Encapsulation of quiz state.
- Separation of data (data.py) from logic (quiz_brain.py).
- Simple control flow within an object.

## How It Works
1. Raw dicts in data.py converted to `Question` objects.
2. `QuizBrain.next_question()` prompts user.
3. Input compared to stored correct answer.
4. Score increments; loop continues until exhausted.

## Run
```bash
python main.py