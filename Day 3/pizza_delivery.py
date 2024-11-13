def calculate_pizza_price():
    try:
        print("Welcome to Python Pizza Deliveries!")
        
        # Get pizza size
        while True:
            size = input("What size pizza do you want? (S/M/L): ").upper()
            if size in ['S', 'M', 'L']:
                break
            print("Please enter S, M, or L")
        
        # Set base price based on size
        if size == "S":
            price = 15
            pepperoni_price = 2
        elif size == "M":
            price = 20
            pepperoni_price = 3
        else:
            price = 25
            pepperoni_price = 3
        
        # Ask for pepperoni
        while True:
            want_pepperoni = input("Do you want pepperoni? (Y/N): ").upper()
            if want_pepperoni in ['Y', 'N']:
                break
            print("Please enter Y or N")
        
        # Add pepperoni cost if selected
        if want_pepperoni == "Y":
            price += pepperoni_price
        
        # Ask for extra cheese
        while True:
            want_cheese = input("Do you want extra cheese? (Y/N): ").upper()
            if want_cheese in ['Y', 'N']:
                break
            print("Please enter Y or N")
        
        # Add cheese cost if selected
        if want_cheese == "Y":
            price += 1
        
        # Print order summary
        print("\n--- Order Summary ---")
        print(f"Size: {'Small' if size == 'S' else 'Medium' if size == 'M' else 'Large'}")
        print(f"Pepperoni: {'Yes' if want_pepperoni == 'Y' else 'No'}")
        print(f"Extra cheese: {'Yes' if want_cheese == 'Y' else 'No'}")
        print(f"Total price: ${price:.2f}")
        
    except KeyboardInterrupt:
        print("\nOrder cancelled. Thank you!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    calculate_pizza_price()