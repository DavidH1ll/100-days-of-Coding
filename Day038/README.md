# Day 38 – Exercise Tracking Application

## Goal
Build an exercise tracker that uses **natural language processing** to interpret workout descriptions and automatically logs them to Google Sheets with date, time, duration, and calories burned.

## Features
- 🗣️ **Natural language input**: "ran 5km and cycled 20 minutes"
- 🔥 **Automatic calorie calculation** based on user profile
- ⏱️ **Duration estimation** for distance-based exercises
- 📊 **Google Sheets integration** for persistent tracking
- 🕐 **Automatic timestamps** (date and time)

## APIs Used

### 1. Nutritionix Natural Language API
**Purpose**: Interprets plain English exercise descriptions and calculates calories.

**Sign up**: https://www.nutritionix.com/business/api
- Free tier: 200 requests/day
- Returns exercise name, duration, calories based on user profile

### 2. Sheety API
**Purpose**: Connects Python to Google Sheets for easy data storage.

**Setup**:
1. Create a Google Sheet with columns: `date`, `time`, `exercise`, `duration`, `calories`
2. Go to https://sheety.co/
3. Connect your Google Sheet
4. Enable POST requests
5. Copy your endpoint URL

## Setup

### 1. Install Dependencies
```bash
pip install requests python-dotenv
```

### 2. Create `.env` File
Copy `.env.example` to `.env` and fill in:

```env
NUTRITIONIX_APP_ID=your_app_id
NUTRITIONIX_API_KEY=your_api_key
SHEETY_ENDPOINT=https://api.sheety.co/username/workouts/workouts
SHEETY_TOKEN=optional_bearer_token

USER_GENDER=male
USER_WEIGHT_KG=70
USER_HEIGHT_CM=175
USER_AGE=30
```

### 3. Run the Application
```bash
python main.py
```

## Usage Examples

**Input:**
```
Tell me which exercises you did: ran 5km and cycled for 20 minutes
```

**Output:**
```
🔍 Processing exercises...

📊 Found 2 exercise(s):
  • Running: 31min, 320 calories
  • Cycling: 20min, 180 calories

📝 Logging to Google Sheets...
✓ Logged: Running - 31min - 320 cal
✓ Logged: Cycling - 20min - 180 cal

✅ All exercises logged successfully!
```

**Google Sheet Result:**
| date       | time     | exercise | duration | calories |
|------------|----------|----------|----------|----------|
| 17/11/2024 | 14:23:45 | Running  | 31       | 320      |
| 17/11/2024 | 14:23:45 | Cycling  | 20       | 180      |

## How It Works

1. **User inputs exercise** in plain English
2. **Nutritionix API** processes the text:
   - Identifies exercises (running, cycling, swimming, etc.)
   - Estimates duration (if distance given)
   - Calculates calories based on user profile
3. **Python script** formats data with current timestamp
4. **Sheety API** adds rows to Google Sheets
5. **Confirmation** printed to console

## Key Concepts

- **Natural Language Processing (NLP)**: AI understands "ran 5km" vs "running for 30 minutes"
- **REST API POST requests**: Sending data to external services
- **Header-based authentication**: Using `x-app-id`, `x-app-key`, and `Bearer` tokens
- **Environment variables**: Keeping secrets secure
- **DateTime formatting**: `strftime()` for date/time strings

## Enhancements

### Easy
- Add error handling for network failures
- Support multiple exercise inputs from file
- Daily summary email

### Medium
- Track weekly/monthly totals
- Charts/graphs from Google Sheets data
- Voice input (using speech recognition)

### Advanced
- Mobile app interface (React Native/Flutter)
- Integration with fitness wearables (Fitbit, Apple Watch)
- Machine learning to predict workout patterns
- Gamification (streaks, badges, challenges)

## Troubleshooting

**"No exercises recognized"**
- Make sure to use clear exercise names (run, cycle, swim, walk)
- Include duration or distance
- Example: "walked 3km" or "swimming for 45 minutes"

**"Missing required environment variables"**
- Check `.env` file exists and is in same directory as `main.py`
- Verify all API credentials are correct
- Restart terminal after creating `.env`

**"Failed to log to Google Sheets"**
- Verify Sheety endpoint URL is correct
- Check sheet permissions (make sure Sheety can edit)
- Verify column names match exactly: `date`, `time`, `exercise`, `duration`, `calories`

## Real-World Applications

- **Personal fitness tracking**: Monitor progress toward goals
- **Coaching tools**: Trainers can track client workouts
- **Research**: Collect exercise data for health studies
- **Insurance/wellness programs**: Verify activity for premium discounts

## Inspiration

Inspired by Simone Giertz's physical habit tracker and OpenAI's GPT-3 natural language capabilities, this project demonstrates how AI can make data entry effortless.

## Next Steps

- **Day 39**: Continue with more advanced API projects
- **Deploy**: Host on PythonAnywhere/Replit for mobile access
- **Integrate**: Connect with other health apps (MyFitnessPal, Strava)