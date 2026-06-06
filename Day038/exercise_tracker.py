"""
Day 38: Exercise Tracking Application
Uses Nutritionix API for natural language exercise processing
and Sheety API to log workouts to Google Sheets.
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Nutritionix API Configuration
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Sheety API Configuration
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")  # Optional: if using authentication

# User info for Nutritionix (affects calorie calculations)
GENDER = os.getenv("USER_GENDER", "male")
WEIGHT_KG = float(os.getenv("USER_WEIGHT_KG", "70"))
HEIGHT_CM = float(os.getenv("USER_HEIGHT_CM", "175"))
AGE = int(os.getenv("USER_AGE", "30"))


def process_exercise(exercise_text: str) -> list:
    """
    Use Nutritionix Natural Language API to process exercise description.
    
    Args:
        exercise_text: Plain English description (e.g., "ran 5km and cycled 20 minutes")
    
    Returns:
        List of exercise dictionaries with name, duration, calories
    """
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    
    body = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }
    
    try:
        response = requests.post(
            NUTRITIONIX_ENDPOINT,
            json=body,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        exercises = []
        for exercise in data.get("exercises", []):
            exercises.append({
                "name": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            })
        
        return exercises
    
    except requests.exceptions.RequestException as e:
        print(f"Error processing exercise: {e}")
        return []


def log_to_sheet(exercises: list) -> bool:
    """
    Log exercises to Google Sheets via Sheety API.
    
    Args:
        exercises: List of exercise dicts from process_exercise()
    
    Returns:
        True if all exercises logged successfully
    """
    if not exercises:
        print("No exercises to log.")
        return False
    
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add Bearer token if configured
    if SHEETY_TOKEN:
        headers["Authorization"] = f"Bearer {SHEETY_TOKEN}"
    
    success_count = 0
    
    for exercise in exercises:
        # Sheety expects data wrapped in a key matching sheet name (usually "workouts")
        body = {
            "workout": {
                "date": date_str,
                "time": time_str,
                "exercise": exercise["name"],
                "duration": exercise["duration"],
                "calories": round(exercise["calories"], 2)
            }
        }
        
        try:
            response = requests.post(
                SHEETY_ENDPOINT,
                json=body,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            print(f"✓ Logged: {exercise['name']} - {exercise['duration']}min - {exercise['calories']:.0f} cal")
            success_count += 1
        
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to log {exercise['name']}: {e}")
    
    return success_count == len(exercises)


def main():
    """Main CLI interface for exercise tracking."""
    print("💪 Exercise Tracker")
    print("=" * 50)
    
    # Check required environment variables
    if not all([NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY, SHEETY_ENDPOINT]):
        print("❌ Missing required environment variables!")
        print("Required: NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY, SHEETY_ENDPOINT")
        return
    
    exercise_input = input("\nTell me which exercises you did: ")
    
    if not exercise_input.strip():
        print("No input provided.")
        return
    
    print("\n🔍 Processing exercises...")
    exercises = process_exercise(exercise_input)
    
    if not exercises:
        print("❌ No exercises recognized. Try rephrasing.")
        return
    
    print(f"\n📊 Found {len(exercises)} exercise(s):")
    for ex in exercises:
        print(f"  • {ex['name']}: {ex['duration']}min, {ex['calories']:.0f} calories")
    
    print("\n📝 Logging to Google Sheets...")
    success = log_to_sheet(exercises)
    
    if success:
        print("\n✅ All exercises logged successfully!")
    else:
        print("\n⚠️ Some exercises failed to log.")


if __name__ == "__main__":
    main()