holes = "abdegopqABDEGOPQ"
answer = 0

word = input("Enter a word: ")
for i in word:
    if i in holes:
        answer += 1
print(answer)