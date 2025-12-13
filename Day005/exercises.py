# Loop through numbers from 1 to 100
for number in range(1, 101):
    # Check if the number is divisible by both 3 and 5
    if number % 3 == 0 and number % 5 == 0:
        print('FizzBuzz')
    # Check if the number is divisible by 3
    elif number % 3 == 0:
        print('Fizz')
    # Check if the number is divisible by 5
    elif number % 5 == 0:
        print('Buzz')
    # If the number is not divisible by 3 or 5, print the number
    else:
        print(number)