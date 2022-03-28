# TODO

class A:

    def __init__(self, value):
        self.value = value

    def __matmul__(self, other):
        print('__matmul__')
        return A(self.value * other.value)

    def __imatmul__(self, other):
        print('__imatmul__')
        self.value *= other.value
        return self


a = A(1)
b = A(2)
print((a @ b).value)

a @= b
print(a.value)