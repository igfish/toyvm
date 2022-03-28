def foo(w):
    print(w)
    i = 5

    def bar(v=9):
        print(w)
        print(i)
        print(v)
    return bar

foo(1)(2)
