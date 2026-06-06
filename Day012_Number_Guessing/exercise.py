def is_prime(number):
    # Edge cases
    if number <= 1:
        return False
    if number == 2:
        return True
    
    # Check if even (except 2)
    if number % 2 == 0:
        return False
        
    # Check odd numbers up to square root
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            return False
            
    return True

# Test cases
test_numbers = [1, 2, 73, 75, 97, 100]
for num in test_numbers:
    print(f"{num} is{' ' if is_prime(num) else ' not '}prime")

# def bar():
#     my_variable = 9
     
#     if 16 > 9:
#         my_variable = 16
#     print(my_variable)
     
# bar()