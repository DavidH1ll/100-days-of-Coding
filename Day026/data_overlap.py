def read_numbers_from_file(filepath):
    with open(filepath) as file:
        return [int(line.strip()) for line in file]

def main():
    # Read numbers from both files
    file1_numbers = read_numbers_from_file('file1.txt')
    file2_numbers = read_numbers_from_file('file2.txt')
    
    # Find common numbers using list comprehension
    result = [number for number in file1_numbers if number in file2_numbers]
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()
