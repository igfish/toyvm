from functools import partial

f = partial(print, 1, 2, 3, 4, 5)
f()