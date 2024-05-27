def calculate_sum(n):
    """
    Function to calculate the sum of numbers from 1 to n using arithmetic progression formula.
    """
    return n * (n + 1) // 2

# Test the function with some examples
if __name__ == "__main__":
    test_values = [1, 2, 3, 4, 5, 10, 20, 100, 1000]
    
    for value in test_values:
        result = calculate_sum(value)
        print(f"The sum of numbers from 1 to {value} is: {result}")