def add(a, b, c=3, d=5):
    print(a)
    print(b)
    print(c)
    print(d)
    return a + b + c + d


print(add(1, 2))
print(add(1, 2, 5))
print(add(1, 2, 5, 6))
