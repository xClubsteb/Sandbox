ACCURACY = 10
BIG_NUMBER = 1000

def factorial(x):
    result = 1
    for i in range(1, x+1):
        result *= i
    return result

def get_e(x):
    e = 0
    for i in range(x):
        e += 1/factorial(i)
    return e

# https://en.wikipedia.org/wiki/E_(mathematical_constant)
print("Euler number approximation using Euler series")
print("e = 1/0! + 1/1! + 1/2! + 1/3! + ... + 1/n! + ...")
print("as n goes to infinity\n")
for i in range(1, ACCURACY+1):
    print(f"sum = {get_e(i):.8f} for n = {i}")

print("\ne approximation using Euler series up to 15th digit:", end=" ")
string = f"{get_e(BIG_NUMBER):.16f}"
new_string = string[:-1]
print(new_string)
