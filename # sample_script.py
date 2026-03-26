# sample_script.py
# Basic Python script for internship repository

def greet(name):
    return f"Hello, {name}! Welcome to SourceSys Technology."

def calculate_square(number):
    return number * number

def main():
    print("=== Internship Demo Script ===")
    
    name = "Likhitha"
    print(greet(name))
    
    num = 5
    print(f"The square of {num} is {calculate_square(num)}")

if __name__ == "__main__":
    main()