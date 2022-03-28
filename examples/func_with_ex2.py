def add(a, b, c, d, *args, **kwargs):
    print(a)
    print(b)
    print(c)
    print(d)
    print(args)
    print(kwargs)
    return a + b + c + d


args = (1, 2, 3, 4, 5, 6)
kwargs = {'z': 3, 'x': 4}
print(add(*args, **kwargs))
