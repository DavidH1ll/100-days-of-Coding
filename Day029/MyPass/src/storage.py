import os

class PasswordStorage:
    def __init__(self, filename="passwords.txt"):
        self.filename = filename

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