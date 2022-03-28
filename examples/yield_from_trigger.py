def foo():
    for i in range(10):
        x = yield i**2
        print('foo:', x)
    return 'foo'


def bar():
    y = yield from foo()
    print('bar:', y)
    return 'bar'


gtor = bar()
print(gtor.send(None))
x = gtor.send(1)
print('x:', x)
x = gtor.send(2)
print('x:', x)
x = gtor.send(3)
print('x:', x)
x = gtor.send(4)
print('x:', x)
x = gtor.send(5)
print('x:', x)
x = gtor.send(1)
print('x:', x)
