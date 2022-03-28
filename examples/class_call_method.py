class Foo:
    value = 1

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def print(self, *args, **kwargs):
        print(self.args)
        print(self.kwargs)
        print(args)
        print(kwargs)


foo = Foo(1, 2, 3, 4, c=5, d=6)
foo.print(1, 2, a=1, b=2)
