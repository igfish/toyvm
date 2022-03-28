def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def add(a, b):
    print(a)
    print(b)
    return a + b


print(add(4, 5))
print(fib(5))  # 0 1 1 2 3 5
