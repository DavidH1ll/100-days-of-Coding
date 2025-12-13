# Day 30 – Exceptions & JSON (Password Manager Improvements)

## Overview
Enhance a password manager by adding robust exception handling and data persistence with JSON.

## Files
- main.py – core app logic (generate, save, retrieve credentials).
- non_existent_file.txt – dummy to trigger FileNotFoundError demo.
- README.md – documentation.

## Concepts Practiced
- try / except / else / finally flow.
- Specific exceptions (KeyError, FileNotFoundError, ValueError).
- Graceful fallbacks (create missing file, return defaults).
- JSON read/write (`json.load`, `json.dump`, ensure file closing).
- Data validation (non-empty fields).
- Updating nested dict structures.

## Typical Data Structure
```json
{
  "example.com": {
    "email": "user@example.com",
    "password": "A1b!2c$"
  }
}
```

## Run
```bash
python main.py
```

## Enhancement Ideas
- Add password strength meter.
- Clipboard auto-copy on generate.
- Merge vs overwrite logic for existing sites.
- Encrypt JSON file (e.g., Fernet).
- Unit tests for load/save helpers.

## Error Handling Pattern (Example)
```python
try:
    with open("data.json") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
```

## Key Takeaway
Structured exception handling + JSON persistence increases resilience and usability of small automation tools.