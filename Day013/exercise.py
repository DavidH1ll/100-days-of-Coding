# Target is the number up to which we count

def fizz_buzz(target):
    for number in range(1, target + 1):
        if number % 3 == 0 and number % 5 == 0:
            print("FizzBuzz")
        elif number % 3 == 0:
            print("Fizz")  # Changed from "Fizz"
        elif number % 5 == 0:
            print("Buzz")  # Changed from "Buzz"
        else:
            print(number)  # Added square brackets

# Test the function
fizz_buzz(100)
