print("HOMEWORK")
print(" " * 3)
print("First task")

a = [1,4,6,7,43,2,1,4,687,0,453,-4454, -54]
b = a[0]
for i in range(len(a)-1):
    if a[i-1] > a[i]:
        b = a[i]
print(b)
print(" ")



print("This is second task")
a = [1, 4, 6, 7, 43, 2, 1, 4, 687, 0, 453, -4454, -54]
b = a[0]
for i in range(1, len(a)):
    if a[i] > b:
        b = a[i]
print(b)
print(" ")



print("This is third task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
value = 5
for i in range(len(a)):
    if a[i] > value:
        a.insert(i, value)
        break
else:
    a.append(value)
print(a)
print(" ")



print("This is forth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
index_to_remove = 5
for i in range(index_to_remove, len(a) - 1):
    a[i] = a[i + 1]
a.pop()
print(a)
print(" ")



print("This is fifth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
n = len(a)
for i in range(n // 2):
    a[i], a[n - i - 1] = a[n - i - 1], a[i]
print(a)
print(" ")



print("This is sixth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    b += i
print(b)
print(" ")




print("This is seventh task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    if i % 2 != 0:
        b += i
print(b)
print(" ")



print("This is eight task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    if i % 2 == 0:
        b += i
print(b)
print(" ")



print("This is ninth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 5
for i in a:
    if i < b:
        print(i)
print(" ")



print("This is tenth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 5
for i in a:
    if i > 5:
        print(i)
print(" ")



print("This is eleventh task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    if i % 2 == 0:
        b += i
    else:
        b -= i
print(b)
print(" ")



print("This is twelfth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
for num in a:
    print('*' * abs(num))
print(" ")



print("This is thirteenth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    b+=1
print(b)
print(" ")



print("This is fourteenth task")
a = [-4454, -54, 0, 1, 1, 2, 4, 4, 6, 7, 43, 453, 687]
b = 0
for i in a:
    b += i
c = b/len(a)
print(c)
print(" ")



print("This is fifteenth task")
words = ["hello", "world", "python", "is", "awesome"]
for i in range(len(words)):
    words[i] = words[i].upper()
print(words)
print(" ")
