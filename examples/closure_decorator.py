def logger(func):
    def wrapper(*args, **kwargs):
        print('---[START]---')
        retval = func(*args, **kwargs)
        print('---[END]---')
        return retval
    return wrapper


@logger
def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


print(fib(5))  # 0 1 1 2 3 5
