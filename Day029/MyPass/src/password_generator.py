import random
import string

try:
    import pyperclip
    _HAS_PYPERCLIP = True
except ImportError:
    _HAS_PYPERCLIP = False

class PasswordGenerator:
    def __init__(self, default_length=16):
        self.default_length = default_length

    def generate_password(self, length=None, use_upper=True, use_digits=True, use_symbols=True):
        if length is None:
            length = self.default_length

        character_pool = string.ascii_lowercase
        if use_upper:
            character_pool += string.ascii_uppercase
        if use_digits:
            character_pool += string.digits
        if use_symbols:
            character_pool += string.punctuation

        if not character_pool:
            raise ValueError("No characters available to generate password.")

        return "".join(random.choice(character_pool) for _ in range(length))

    def copy_to_clipboard(self, password):
        if _HAS_PYPERCLIP:
            pyperclip.copy(password)
        else:
            # Fallback to tkinter clipboard
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(password)
                root.update()
                root.destroy()
            except Exception:
                pass