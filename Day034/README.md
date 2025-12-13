# Day 34 - Quizzler Quiz App

A trivia quiz application using the Open Trivia Database API and tkinter for the graphical interface.

## Overview

Quizzler fetches true/false questions from the Open Trivia Database and presents them in a clean GUI. Users can answer questions by clicking True or False buttons, with immediate visual feedback and score tracking.

## Features

- **API Integration**: Fetches questions from [Open Trivia Database](https://opentdb.com/)
- **Interactive GUI**: Built with tkinter for a smooth user experience
- **Visual Feedback**: Canvas changes color (green/red) based on answer correctness
- **Score Tracking**: Real-time score display throughout the quiz
- **Customizable**: Adjust number of questions, category, and difficulty
- **HTML Decoding**: Properly displays special characters in questions

## Project Structure

```
Day034/
├── Main.py              # Entry point - orchestrates the app
├── data.py              # API data fetcher
├── question_model.py    # Question class model
├── quiz_brain.py        # Quiz logic and scoring
├── ui.py                # Tkinter GUI interface
├── images/              # Placeholder for custom button images
└── README.md
```

## Requirements

- Python 3.x
- `requests` library

Install dependencies:
```powershell
pip install requests
```

## Usage

Run the application:
```powershell
python Main.py
```

Or from the project root:
```powershell
python .\Day034\Main.py
```

## Customization

Edit `Main.py` to customize quiz parameters:

```python
question_data = fetch_questions(
    amount=10,           # Number of questions (1-50)
    category=18,         # Category ID (None for random)
    difficulty="medium", # "easy", "medium", "hard", or None
    question_type="boolean"
)
```

### Popular Categories

- `9` - General Knowledge
- `18` - Science: Computers
- `21` - Sports
- `22` - Geography
- `23` - History

[View all categories](https://opentdb.com/api_category.php)

## How It Works

1. **Fetch Questions**: `data.py` sends a GET request to the Open Trivia DB API
2. **Create Models**: Questions are converted to `Question` objects
3. **Initialize Quiz**: `QuizBrain` manages question flow and scoring
4. **Launch GUI**: `QuizInterface` displays questions and handles user input
5. **Visual Feedback**: Canvas color changes based on answer correctness
6. **Final Score**: Shows results when all questions are answered

## API Details

The app uses the Open Trivia Database API:
- **Endpoint**: `https://opentdb.com/api.php`
- **Parameters**: amount, category, difficulty, type
- **Response**: JSON with questions and answers
- **Decoding**: HTML entities are automatically decoded

## UI Features

- **Question Display**: White canvas with centered question text
- **True Button**: Green button on the left
- **False Button**: Red button on the right
- **Score Label**: Top-right corner shows current score
- **Feedback**: 1-second color flash after each answer
- **Final Screen**: Shows total score when quiz ends

## Error Handling

- Network errors are caught and logged
- API response codes are validated
- Graceful fallback if questions can't be fetched
- Buttons disabled during answer feedback

## Future Enhancements

- Add multiple choice question support
- Implement difficulty progression
- Save high scores to file
- Add timer for each question
- Custom button images (true.png, false.png)
- Sound effects for correct/incorrect answers
- Question history/review mode

---

Built as part of the 100 Days of Code Python challenge.
