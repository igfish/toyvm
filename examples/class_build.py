class Foo:
    value = 1

    def __init__(self):
        self.value = 2

    def print(self):
        print(self.value)


foo = Foo()
foo.print()
