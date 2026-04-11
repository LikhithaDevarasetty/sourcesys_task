def discount_calculator(discount):
    def apply_discount(price):
        return price - (price * discount / 100)
    return apply_discount

ten_percent = discount_calculator(10)
twenty_percent = discount_calculator(20)

print("10% Discount:", ten_percent(1000))
print("20% Discount:", twenty_percent(1000))