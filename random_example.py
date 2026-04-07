import random

def generate_random_number():
    try:
        num = random.randint(1, 10)
        print("Random number:", num)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    generate_random_number()