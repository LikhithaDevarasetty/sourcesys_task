def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    else:
        print("Result:", result)
    finally:
        print("Division operation done\n")

if __name__ == "__main__":
    divide(10, 2)
    divide(10, 0)