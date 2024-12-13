def accept_any_number_except_five(number):
    if number < 5:
        raise ValueError("Numbers lower than 5 are not accepted.")
    return f"The number {number} is accepted."

while True:
    try:
        user_input = int(input("Enter a number: "))
        print(accept_any_number_except_five(user_input))
        for i in range(user_input + 1, user_input + 6):
            print(accept_any_number_except_five(i))
        break
    except ValueError as e:
        print(e)