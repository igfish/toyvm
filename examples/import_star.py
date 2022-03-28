from functools import *

f = partial(print, 1, 2, 3, 4, 5)
f()