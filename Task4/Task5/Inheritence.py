class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def show_details(self):
        print(f"Name: {self.name}, Salary: {self.salary}")

class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def show_details(self):
        print(f"Developer: {self.name}, Salary: {self.salary}, Language: {self.language}")

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def show_details(self):
        print(f"Manager: {self.name}, Salary: {self.salary}, Team Size: {self.team_size}")

if __name__ == "__main__":
    d1 = Developer("Likhitha", 60000, "Python")
    m1 = Manager("Namitha", 80000, 5)

    d1.show_details()
    m1.show_details()