def read_file_lines(filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print("File not found")

for line in read_file_lines("Task6/likhitha.txt"):
    print("Line:", line)