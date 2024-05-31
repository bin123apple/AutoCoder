def sum_numbers(n):
    total = 0
    for i in range(n + 1):
        total += i
    return total

def main():
    n = 10  # Predefined value for n
    result = sum_numbers(n)
    print(f"The sum of numbers from 1 to {n} is: {result}")

if __name__ == "__main__":
    main()