from abc import ABC, abstractmethod
# Abstract class
class Shape(ABC):

    @abstractmethod
    def area(self):
        pass
# Child class
class Rectangle(Shape):

    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
    def area(self):
        print("Area:", self.length * self.breadth)     
if __name__ == "__main__":
    r1 = Rectangle(10, 5)
    r1.area()