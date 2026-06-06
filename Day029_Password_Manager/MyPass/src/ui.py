from tkinter import Label, Entry, Button, messagebox, Canvas, PhotoImage
import tkinter as tk

class MyPassUI:
    def __init__(self, master, password_generator=None, password_storage=None, validator=None):
        self.master = master
        self.password_generator = password_generator
        self.password_storage = password_storage
        self.validator = validator

        master.title("MyPass - Password Manager")
        master.config(padx=50, pady=50)

        # Logo/Canvas
        self.canvas = Canvas(master, width=200, height=200)
        try:
            self.logo_img = PhotoImage(file="logo.png")
            self.canvas.create_image(100, 100, image=self.logo_img)
        except:
            self.canvas.create_text(100, 100, text="🔐", font=("Arial", 60))
        self.canvas.grid(row=0, column=1)

        # Website Label and Entry
        self.website_label = Label(master, text="Website:")
        self.website_label.grid(row=1, column=0, sticky="e")
        
        self.website_entry = Entry(master, width=21)
        self.website_entry.grid(row=1, column=1, sticky="ew")
        self.website_entry.focus()

        # Search Button
        self.search_button = Button(master, text="Search", command=self.search_password)
        self.search_button.grid(row=1, column=2, sticky="ew")

        # Email/Username Label and Entry
        self.email_label = Label(master, text="Email/Username:")
        self.email_label.grid(row=2, column=0, sticky="e")
        
        self.email_entry = Entry(master, width=35)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.email_entry.insert(0, "your@email.com")  # Default email

        # Password Label and Entry
        self.password_label = Label(master, text="Password:")
        self.password_label.grid(row=3, column=0, sticky="e")
        
        self.password_entry = Entry(master, width=21)
        self.password_entry.grid(row=3, column=1, sticky="ew")

        # Generate Password Button
        self.generate_button = Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=3, column=2, sticky="ew")

        # Add Button
        self.add_button = Button(master, text="Add", width=36, command=self.save_password)
        self.add_button.grid(row=4, column=1, columnspan=2, sticky="ew")

    def generate_password(self):
        """Generate a random password and insert it into the password field"""
        if self.password_generator:
            password = self.password_generator.generate_password(length=12)
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, password)
            try:
                self.password_generator.copy_to_clipboard(password)
                messagebox.showinfo("Success", "Password generated and copied to clipboard!")
            except Exception:
                messagebox.showinfo("Success", "Password generated!")
        else:
            self.password_entry.delete(0, 'end')
            self.password_entry.insert(0, "GeneratedPassword123!")

    def save_password(self):
        """Save the password entry after validation"""
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate all fields
        if not self.validator or not self.validator.validate_all(website, email, password):
            messagebox.showwarning("Warning", "Please don't leave any fields empty!")
            return

        # Confirm before saving
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\n\nIs it ok to save?"
        )

        if is_ok:
            if self.password_storage:
                self.password_storage.add_password(website, email, password)
                messagebox.showinfo("Success", "Password saved successfully!")
                
                # Clear the fields
                self.website_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')

    def search_password(self):
        """Search for a password by website name"""
        website = self.website_entry.get()
        
        if not website:
            messagebox.showwarning("Warning", "Please enter a website name to search!")
            return
        
        if self.password_storage:
            result = self.password_storage.search_password(website)
            
            if result:
                self.email_entry.delete(0, 'end')
                self.email_entry.insert(0, result["email"])
                self.password_entry.delete(0, 'end')
                self.password_entry.insert(0, result["password"])
                
                # Copy password to clipboard
                if self.password_generator:
                    try:
                        self.password_generator.copy_to_clipboard(result["password"])
                    except Exception:
                        pass
                
                messagebox.showinfo("Found", f"Password found for {website}!\nPassword copied to clipboard.")
            else:
                messagebox.showinfo("Not Found", f"No password found for {website}.")

def create_ui(root, password_generator, password_storage, validator):
    """Create and return the UI instance"""
    return MyPassUI(root, password_generator, password_storage, validator)