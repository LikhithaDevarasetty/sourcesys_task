import math

def calculate_square_root(num):
    try:
        result = math.sqrt(num)
    except ValueError:
        print("Error: Cannot calculate square root of negative number")
    else:
        print(f"Square root of {num} is {result}")
    finally:
        print("Execution completed\n")

if __name__ == "__main__":
    calculate_square_root(25)
    calculate_square_root(-5)