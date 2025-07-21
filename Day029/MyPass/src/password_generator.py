import random
import string
import pyperclip


class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.include_uppercase = True
        self.include_numbers = True
        self.include_special = True

    def generate_password(self):
        character_pool = string.ascii_lowercase
        if self.include_uppercase:
            character_pool += string.ascii_uppercase
        if self.include_numbers:
            character_pool += string.digits
        if self.include_special:
            character_pool += string.punctuation

        password = ''.join(random.choice(character_pool) for _ in range(self.length))
        return password

    def copy_to_clipboard(self, password):
        pyperclip.copy(password)