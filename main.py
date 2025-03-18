print(" ")
print("EXERCISE IN THE CLASS")
print(" " * 3)


print("This is first task")
radius = 5
side = 4
P = 3.14

area_of_circle = P * radius* radius
area_of_square = side ** 2
difference = max(area_of_circle, area_of_square) - min(area_of_circle, area_of_square)
print(difference)
print(" ")



print("This is a second task")
x = int(input("Write the number: "))

if x % 2 == 0 and x % 3 == 0:
    print("x divided by 2 and 3")
elif x % 2 == 0 and x % 3 != 0:
    print("x divided by 2, but not by 3")
elif x % 3 == 0 and x % 2 != 0:
    print("x divided by 3, but not by 2")
else:
    print("x dont diveded by 2 or 3")
print(" ")


print("This is a third task")
r = 5
P = 3.14
volume = 4/3 * P * r ** 3
print(volume)
print(" ")



print("This is a forth task")
order = 60
first_copy = 3
next_copy = 0.75
price = 24.95
discount = 0.4

cost = ((price + first_copy) + (next_copy*(order - 1) + (price*(order - 1)) )) * (1 - discount)
different_cost = (price * (1 - discount) + first_copy) + (next_copy * (order - 1) + (price*(1 - discount) * (order - 1)) )
print(cost)
print(different_cost)
print(" ")


print(" " * 5)
print("HOMEWORK")
print(" " * 3)
print("First task")
x = int(input("Write the number: "))
if x > 10:
    print("x is greater than 10")
elif x == 10:
    print("x is equal than 10")
else:
    print("x is less than 10")
print(" ")



print("This is second task")
word = input("Write the word: ")
if word == "Pyhton":
    print("The word was Python")
else:
    print("The word wasnt Python")
print(" ")



print("This is third task")
price = float(input("Enter the price: €"))
if price >= 9.99:
    print(f"The price (€{price:.2f}) is greater than or equal to €9.99.")
else:
    print(f"The price (€{price:.2f}) is less than €9.99.")
print(" ")



print("This is forth task")
fruit = {"apple", "banana", "pineapple"}
fruit_name = input("Write a fruit name with small letter: ")
if fruit_name in fruit:
    print("Your fruit in tuple")
else:
    print("Your fruit not in tuple")
print(" ")



print("This is fifth task")
name = ["Max", "Liza", "Georg"]
your_name = input("Write your name: ")
if your_name in name:
    print("Your name in list")
else:
    print("Your name not in list")
print(" ")



print("This is sixth task")
code = input("Write code for examle JDFEOE: ")
if code[:3] == "ABC":
    print("Your code starts with ABC")
else:
    print("Your code doesnt start with ABC")
print(" ")




print("This is seventh task")
y = None
if y == None:
    print("The variable is equal None")
print(" ")



print("This is eight task")
text = "Hello, world!\nThis is a new line."
if "\n" in text:
    print("The string contains a newline character.")
else:
    print("The string does not contain a newline character.")
print(" ")



print("This is ninth task")
grade = input("Write you grade in precentage: ")
if grade >= 90:
    print("Exelent")
elif grade < 90 and grade >= 75:
    print("Good")
else:
    print("Needs improvements")
print(" ")



print("This is tenth task")
age = int(input("Write you age here"))
if age > 18:
    print("Older than 18")
elif age == 18:
    print("18 years old")
else:
    print("Younger than 18")
print(" ")



print("This is eleventh task")
temperature = int(input("Write your temperature: "))
if 20 < temperature < 30:
    print("Your temperature between 20 and 30")
else:
    print("Your temperature isnt between 20 and 30")
print(" ")




