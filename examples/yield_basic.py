def foo():
    for i in range(10):
        yield i**2


for i in foo():
    print(i)
