from tkinter import Tk, Label, Entry, Button, messagebox, StringVar

class MyPassUI:
    def __init__(self, master, password_generator=None, password_storage=None, validator=None):
        self.master = master
        self.password_generator = password_generator
        self.password_storage = password_storage
        self.validator = validator

        master.title("MyPass - Password Manager")

        self.label = Label(master, text="Password Manager")
        self.label.pack()

        self.password_label = Label(master, text="Generated Password:")
        self.password_label.pack()

        self.password_entry = Entry(master, width=50)
        self.password_entry.pack()

        self.generate_button = Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.save_button = Button(master, text="Save Password", command=self.save_password)
        self.save_button.pack()

        self.status = StringVar()
        self.status_label = Label(master, textvariable=self.status)
        self.status_label.pack()

    def generate_password(self):
        if self.password_generator:
            password = self.password_generator.generate_password()
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, password)
            try:
                self.password_generator.copy_to_clipboard(password)
            except Exception:
                pass
        else:
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, "GeneratedPassword123!")  # Example password

    def save_password(self):
        password = self.password_entry.get()
        if password:
            if self.password_storage:
                self.password_storage.add_password("website", "username", password)
            self.status.set("Password saved successfully!")
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            self.status.set("Please generate a password first.")
            messagebox.showwarning("Warning", "Please generate a password first.")

def create_ui(root, password_generator, password_storage, validator):
    MyPassUI(root, password_generator, password_storage, validator)

def main():
    root = Tk()
    my_pass_ui = MyPassUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()