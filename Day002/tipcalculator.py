def calculate_tip():
    try:
        # Get bill amount
        bill = float(input("What is your bill total? $"))
        
        # Get tip percentage
        tip_percent = float(input("What percentage tip would you like to give? (10, 15, 20): "))
        
        # Get number of people
        num_people = int(input("How many people are splitting the bill? "))
        
        if num_people <= 0:
            raise ValueError("Number of people must be positive!")
        
        # Calculate amounts
        tip_amount = bill * (tip_percent / 100)
        total = bill + tip_amount
        
        # Calculate per person amounts
        bill_per_person = bill / num_people
        tip_per_person = tip_amount / num_people
        total_per_person = total / num_people
        
        # Format and display results
        print("\n--- Summary ---")
        print(f"Bill Amount: ${bill:.2f}")
        print(f"Tip Percentage: {tip_percent}%")
        print(f"Tip Amount: ${tip_amount:.2f}")
        print(f"Total Amount: ${total:.2f}")
        print(f"\n--- Per Person ---")
        print(f"Bill per person: ${bill_per_person:.2f}")
        print(f"Tip per person: ${tip_per_person:.2f}")
        print(f"Total per person: ${total_per_person:.2f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Welcome to the Tip Calculator!")
    calculate_tip()