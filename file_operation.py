def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print("File Content:\n", content)
    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    read_file("sample.txt")   