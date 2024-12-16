def calculate_love_score():
    try:
        # Get input for both names
        name1 = input("Enter first name: ")
        name2 = input("Enter second name: ")
        
        # Validate inputs
        if not name1 or not name2:
            print("Please enter both names!")
            return
            
        # Combine names and convert to uppercase
        combined_names = (name1 + name2).upper()
        
        # Count TRUE occurrences
        true_count = 0
        for char in "TRUE":
            true_count += combined_names.count(char)
            
        # Count LOVE occurrences
        love_count = 0
        for char in "LOVE":
            love_count += combined_names.count(char)
            
        # Combine scores into 2-digit number
        love_score = int(str(true_count) + str(love_count))
        
        # Print result with names
        print(f"The love score for {name1} and {name2} is: {love_score}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Run the calculator
if __name__ == "__main__":
    calculate_love_score()