# Define the NATO alphabet dictionary
nato_alphabet = {
    'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo', 'F': 'Foxtrot',
    'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett', 'K': 'Kilo', 'L': 'Lima',
    'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo',
    'S': 'Sierra', 'T': 'Tango', 'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
    'Y': 'Yankee', 'Z': 'Zulu'
}

def spell_with_nato(word):
    # Convert the word to uppercase
    word = word.upper()
    # Spell out the word using the NATO alphabet
    spelled_word = [nato_alphabet[letter] for letter in word if letter in nato_alphabet]
    return ' '.join(spelled_word)

def main():
    # Get user input
    word = input("Enter a word to spell out using the NATO alphabet: ")
    # Spell out the word
    result = spell_with_nato(word)
    # Print the result
    print(result)

if __name__ == "__main__":
    main()
