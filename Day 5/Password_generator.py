import random
import string

def generate_password():
    try:
        print("Welcome to the PyPassword Generator!")
        
        # Get password length
        length = int(input("How many characters would you like in your password? "))
        if length <= 0:
            raise ValueError("Password length must be positive!")
            
        # Get character type preferences
        want_letters = input("Include letters? (y/n): ").lower() == 'y'
        want_numbers = input("Include numbers? (y/n): ").lower() == 'y'
        want_symbols = input("Include symbols? (y/n): ").lower() == 'y'
        
        # Create character pool based on preferences
        chars = ''
        if want_letters:
            chars += string.ascii_letters
        if want_numbers:
            chars += string.digits
        if want_symbols:
            chars += string.punctuation
            
        if not chars:
            raise ValueError("You must select at least one character type!")
            
        # Generate password
        password = ''.join(random.choice(chars) for _ in range(length))
        
        print("\nYour generated password is:")
        print(f"🔐 {password} 🔐")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    generate_password()