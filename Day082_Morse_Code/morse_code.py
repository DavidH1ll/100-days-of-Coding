import os

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', ' ': '/'
}

MORSE_TO_TEXT = {v: k for k, v in MORSE_CODE.items()}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_logo():
    logo = r'''
 __  __                  ____          _
|  \/  | ___  _ __ ___  / ___|___   __| | ___
| |\/| |/ _ \| '__/ __|| |   / _ \ / _` |/ _ \
| |  | | (_) | |  \__ \| |__| (_) | (_| |  __/
|_|  |_|\___/|_|  |___/ \____\___/ \__,_|\___|

'''
    print(logo)


def text_to_morse(text):
    output = []
    for char in text.upper():
        if char in MORSE_CODE:
            output.append(MORSE_CODE[char])
    return ' '.join(output)


def morse_to_text(morse):
    output = []
    words = morse.strip().split(' / ')
    for word in words:
        letters = word.split(' ')
        decoded = []
        for letter in letters:
            if letter in MORSE_TO_TEXT:
                decoded.append(MORSE_TO_TEXT[letter])
        output.append(''.join(decoded))
    return ' '.join(output)


def morse_converter():
    clear_screen()
    display_logo()
    print("Welcome to the Morse Code Converter!\n")

    while True:
        print("Choose an option:")
        print("  1. Text to Morse Code")
        print("  2. Morse Code to Text")
        print("  3. Quit")

        try:
            choice = input("\nEnter your choice (1/2/3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if choice == '1':
            print("\n--- Text to Morse Code ---")
            text = input("Enter the text to convert: ")
            result = text_to_morse(text)
            print(f"\nMorse Code:\n{result}")
            input("\nPress Enter to continue...")
            clear_screen()
            display_logo()

        elif choice == '2':
            print("\n--- Morse Code to Text ---")
            print("Use '.' for dot, '-' for dash, space between letters,")
            print("and ' / ' (space-slash-space) between words.")
            morse = input("Enter the Morse Code: ")
            try:
                result = morse_to_text(morse)
                print(f"\nDecoded Text:\n{result}")
            except Exception as e:
                print(f"\nError decoding Morse Code. Make sure you've used the correct format.")
            input("\nPress Enter to continue...")
            clear_screen()
            display_logo()

        elif choice == '3':
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to continue...")
            clear_screen()
            display_logo()


if __name__ == "__main__":
    try:
        morse_converter()
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
