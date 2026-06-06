def check_ticket_price():
    try:
        print("Welcome to the Theme Park Ticket System!")
        print("(Press Ctrl+C to exit at any time)\n")
        
        # Get height from user with validation loop
        while True:
            try:
                height_input = input("Enter your height in cm (or 'q' to quit): ")
                if height_input.lower() == 'q':
                    print("Thank you for using our system!")
                    return
                    
                height = float(height_input)
                if height <= 0:
                    print("Height must be positive!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for height!")
            
        # Check height requirement
        if height < 120:
            print("Sorry, you must be at least 120cm tall to ride.")
            return
            
        # Get age with validation loop
        while True:
            try:
                age_input = input("Enter your age (or 'q' to quit): ")
                if age_input.lower() == 'q':
                    print("Thank you for using our system!")
                    return
                    
                age = int(age_input)
                if age <= 0:
                    print("Age must be positive!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for age!")
            
        # Determine base ticket price based on age
        if 45 <= age <= 55:
            price = 0
            print("Congratulations! Riders between 45-55 ride for FREE!")
        elif age < 12:
            price = 5
            print(f"Child ticket price: ${price:.2f}")
        elif age < 18:
            price = 7
            print(f"Youth ticket price: ${price:.2f}")
        else:
            price = 12
            print(f"Adult ticket price: ${price:.2f}")
        
        # Photo option with validation loop
        while True:
            photo_choice = input("Would you like to add a photo for $3? (yes/no or 'q' to quit): ").lower()
            if photo_choice == 'q':
                print("Thank you for using our system!")
                return
            if photo_choice in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'")
        
        # Add photo cost if selected
        if photo_choice == 'yes':
            price += 3
            print(f"Final price with photo: ${price:.2f}")
        else:
            print(f"Final price: ${price:.2f}")
            
    except KeyboardInterrupt:
        print("\nProgram terminated. Thank you for using our system!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please try again.")

if __name__ == "__main__":
    check_ticket_price()