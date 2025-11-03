word = input("Введите текст: ")
new_text = ""
for i in word:
    if i == "Л":
        new_text += "Р"
    elif i == "л":
        new_text += "р"    
    else:
        new_text += i
print(new_text)