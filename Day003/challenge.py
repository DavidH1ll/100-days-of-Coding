# Get user input with validation
try:
    weight = float(input("Enter your weight in kg: "))
    height_input = float(input("Enter your height in cm: "))
    
    # Convert height to meters
    height = height_input / 100
    
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive numbers!")
    
    bmi = weight / (height ** 2)
    bmi = round(bmi, 1)
    
    # Interpret BMI values
    if bmi < 18.5:
        print(f"Your BMI is {bmi}, you are underweight")
    elif 18.5 <= bmi < 25:
        print(f"Your BMI is {bmi}, you have normal weight")
    else:
        print(f"Your BMI is {bmi}, you are overweight")
        
except ValueError as e:
    print(f"Error: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
