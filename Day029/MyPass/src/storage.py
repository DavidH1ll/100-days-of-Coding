import os
from pathlib import Path

class PasswordStorage:
    def __init__(self, filename="passwords.txt"):
        # Get the Day029 folder (parent of src folder)
        day029_folder = Path(__file__).parent.parent
        self.filename = day029_folder / filename

    def add_password(self, website, email, password):
        """Save password entry to file"""
        with open(self.filename, "a") as file:
            file.write(f"{website} | {email} | {password}\n")

    def get_all_passwords(self):
        """Retrieve all stored passwords"""
        if not os.path.exists(self.filename):
            return []
        
        with open(self.filename, "r") as file:
            return file.readlines()

    def search_password(self, website):
        """Search for a password by website name"""
        if not os.path.exists(self.filename):
            return None
        
        with open(self.filename, "r") as file:
            for line in file:
                parts = line.strip().split(" | ")
                if len(parts) == 3 and parts[0].lower() == website.lower():
                    return {"website": parts[0], "email": parts[1], "password": parts[2]}
        return None