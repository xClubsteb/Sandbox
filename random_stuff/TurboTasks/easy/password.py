import random

length = int(input("Length: "))
symbols = input("Symbols for password: ")

symbols = list(set(symbols))
amount = len(symbols)

password = ""
for i in range(length):
    rand_index = random.randint(0, amount-1)
    password += symbols[rand_index]

print(password)
