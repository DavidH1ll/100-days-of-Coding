"""
Customer acquisition module - handles user sign-up and validation.
"""

import os
import re
import requests

SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT", "")
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN", "")


class CustomerAcquisition:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"} if SHEETY_TOKEN else {}
    
    def validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_name(self, name: str) -> bool:
        """Validate name (letters, spaces, hyphens only)."""
        pattern = r'^[a-zA-Z\s\-]+$'
        return len(name) >= 2 and re.match(pattern, name) is not None
    
    def add_user(self, first_name: str, last_name: str, email: str) -> bool:
        """Add user to Google Sheets via Sheety."""
        if not SHEETY_USERS_ENDPOINT:
            print("❌ SHEETY_USERS_ENDPOINT not configured.")
            return False
        
        body = {
            "user": {
                "firstName": first_name.title(),
                "lastName": last_name.title(),
                "email": email.lower()
            }
        }
        
        try:
            response = requests.post(
                SHEETY_USERS_ENDPOINT,
                json=body,
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            print(f"✅ Successfully added {first_name} {last_name} to Flight Club!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to add user: {e}")
            return False
    
    def register_users(self):
        """Interactive CLI for registering multiple users."""
        print("\n🎯 Welcome to Flight Club!")
        print("Get daily emails with the cheapest flight deals.\n")
        
        while True:
            print("-" * 60)
            
            while True:
                first_name = input("First Name: ").strip()
                if self.validate_name(first_name):
                    break
                print("❌ Invalid name. Use letters, spaces, or hyphens only.")
            
            while True:
                last_name = input("Last Name: ").strip()
                if self.validate_name(last_name):
                    break
                print("❌ Invalid name. Use letters, spaces, or hyphens only.")
            
            while True:
                email = input("Email: ").strip()
                if not self.validate_email(email):
                    print("❌ Invalid email format. Try again.")
                    continue
                
                email_confirm = input("Confirm Email: ").strip()
                if email.lower() == email_confirm.lower():
                    break
                print("❌ Emails don't match. Try again.")
            
            self.add_user(first_name, last_name, email)
            
            more = input("\nRegister another user? (y/n): ").strip().lower()
            if more != 'y':
                print("\n✅ Registration complete!")
                break
