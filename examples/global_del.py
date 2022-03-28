x = 1


def foo():
    global x
    print(x)
    del x
    # print(x)

foo()
