import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def caesar_cipher():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    try:
        clear_screen()
        print("Welcome to Caesar Cipher!")
        print("------------------------\n")
        
        # Get user choice
        direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
        if direction not in ['encode', 'decode']:
            raise ValueError("Please choose 'encode' or 'decode'")
        
        # Get message and shift amount
        text = input("Type your message:\n").lower()
        shift = int(input("Type the shift number:\n"))
        
        # Normalize shift to handle large numbers
        shift = shift % 26
        
        # Reverse shift if decoding
        if direction == "decode":
            shift *= -1
        
        # Process each character
        result = ""
        for char in text:
            if char in alphabet:
                # Find current index and calculate new position
                position = alphabet.index(char)
                new_position = (position + shift) % 26
                result += alphabet[new_position]
            else:
                # Keep non-alphabet characters unchanged
                result += char
        
        print(f"\nThe {direction}d text is: {result}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    print("Welcome to Caesar Cipher!")
    print("------------------------")
    caesar_cipher()