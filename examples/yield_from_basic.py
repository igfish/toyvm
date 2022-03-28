def foo():
    for i in range(10):
        yield i**2


def bar():
    yield from foo()


for i in bar():
    print(i)
