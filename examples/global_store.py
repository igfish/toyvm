x = 1


def foo():
    global x
    print(x)
    x = 2
    print(x)


foo()
