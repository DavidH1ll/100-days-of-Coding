"""
Day 070 - Repository Maintenance & Security Hardening
======================================================

This day was dedicated to improving the overall quality, consistency,
and security of the entire 100 Days of Coding repository.

Run this script to get a summary of the repository's day coverage.
"""

import os


def get_day_folders(base_path: str = ".") -> list[str]:
    """Return a sorted list of all DayXXX folders in the repository."""
    return sorted(
        entry for entry in os.listdir(base_path)
        if entry.startswith("Day") and os.path.isdir(os.path.join(base_path, entry))
    )


def check_day_folder(day_path: str) -> dict:
    """Check a day folder for key files and return a status dict."""
    contents = set(os.listdir(day_path))
    return {
        "has_main": "main.py" in contents,
        "has_readme": "README.md" in contents,
        "has_requirements": "requirements.txt" in contents,
        "has_env_example": ".env.example" in contents,
    }


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    days = get_day_folders(repo_root)
    print(f"Total day folders: {len(days)}\n")

    missing_readme = []
    missing_main = []

    for day in days:
        day_path = os.path.join(repo_root, day)
        status = check_day_folder(day_path)
        if not status["has_readme"]:
            missing_readme.append(day)
        if not status["has_main"]:
            missing_main.append(day)

    if missing_readme:
        print(f"Days missing README.md ({len(missing_readme)}): {', '.join(missing_readme)}")
    else:
        print("All day folders have a README.md")

    if missing_main:
        print(f"Days missing main.py ({len(missing_main)}): {', '.join(missing_main)}")
    else:
        print("All day folders have a main.py")

    print(f"\nRepository maintenance complete. {len(days)} days covered.")


if __name__ == "__main__":
    main()
