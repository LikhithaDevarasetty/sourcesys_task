class Student:
    
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def display(self):
        print("Name:", self.name)
        print("Marks:", self.marks)

if __name__ == "__main__":
    s1 = Student("Likhitha", 90)
    s1.display()