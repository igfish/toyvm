def add(a, b, c, d):
    print(a)
    print(b)
    print(c)
    print(d)
    return a + b + c + d


args = (1, 2)
kwargs = {'c': 3, 'd': 4}
print(add(*args, **kwargs))
