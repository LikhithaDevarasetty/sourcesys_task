class Bank:
    
    def __init__(self, balance):
        self.__balance = balance   # private variable

    def deposit(self, amount):
        self.__balance += amount
        print("Deposited:", amount)

    def get_balance(self):
        return self.__balance


if __name__ == "__main__":
    b1 = Bank(1000)
    b1.deposit(500)
    print("Balance:", b1.get_balance())