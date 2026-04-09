class Bird:
    def sound(self):
        print("Bird makes sound")

class Parrot(Bird):
    def sound(self):
        print("Parrot speaks")

class Crow(Bird):
    def sound(self):
        print("Crow caws")

if __name__ == "__main__":
    for bird in [Parrot(), Crow()]:
        bird.sound()