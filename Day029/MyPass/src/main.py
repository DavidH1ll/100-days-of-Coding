# filepath: MyPass/MyPass/src/main.py

import tkinter as tk
from ui import create_ui
from password_generator import PasswordGenerator
from storage import PasswordStorage
from validation import Validator

class MyPass:
    def __init__(self, root):
        self.root = root
        self.root.title("MyPass - Password Manager")
        
        self.password_generator = PasswordGenerator()
        self.password_storage = PasswordStorage()
        self.validator = Validator()

        create_ui(self.root, self.password_generator, self.password_storage, self.validator)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyPass(root)
    root.mainloop()