# TODO: Create the logging_decorator() function 👇
def logging_decorator(function):
    def wrapper(*args):
        # Get the function name
        func_name = function.__name__
        # Call the function and get the result
        result = function(*args)
        # Print the log message
        print(f"You called {func_name}{args}")
        print(f"It returned: {result}")
        return result
    return wrapper


# TODO: Use the decorator 👇
@logging_decorator
def a_function(*args):
    return sum(args)
    
a_function(1,2,3)