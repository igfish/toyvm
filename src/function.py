import inspect
from collections.abc import Coroutine as CoroutineBase
from functools import partial
from types import CodeType, FunctionType
from typing import Any


def make_cell(value):
    # Thanks to Alex Gaynor for help with this bit of twistiness.
    # Construct an actual cell object by creating a closure right here,
    # and grabbing the cell object out of the function we create.
    fn = (lambda x: lambda: x)(value)
    return fn.__closure__[0]


class Cell:
    def __init__(self, value: Any):
        self.value = value


class CodeFlag:
    OPTIMIZED = 0x0001
    NEWLOCALS = 0x0002
    VARARGS = 0x0004
    VARKEYWORDS = 0x0008
    NESTED = 0x0010
    GENERATOR = 0x0020
    COROUTINE = 0x0080


class Function:

    def __init__(self, name: str, code: CodeType, globals: dict[str, Any],
                 defaults: tuple[Any] = (), closure: tuple[Cell] = (), interpreter=None) -> None:
        self.func_name = name
        self.func_code = code

        self.func_globals = globals
        self.func_defaults = defaults
        self.func_closure = closure

        helper_closure = tuple(make_cell(0) for c in closure)
        self._helper = FunctionType(code, globals, name, defaults, helper_closure)
        self._interpreter = interpreter

    @property
    def code(self):
        return self.func_code

    @property
    def globals(self):
        return self.func_globals

    @property
    def closure(self):
        return self.func_closure

    @property
    def defaults(self):
        return self.func_defaults

    @property
    def argcount(self):
        return self.func_code.co_argcount

    @property
    def varnames(self):
        return self.func_code.co_varnames

    def __repr__(self):
        return '<Function {}>'.format(repr(self.func_name))

    def __get__(self, instance, owner):
        if instance is not None:
            return partial(self, instance)
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        callargs = inspect.getcallargs(self._helper, *args, **kwargs)
        args = [... for _ in range(len(callargs))]
        i = 0
        for name in self.code.co_varnames:
            if name in callargs:
                args[i] = callargs.pop(name)
                i += 1
        for value in callargs.values():
            args[i] = value
            i += 1
        frame = self._interpreter.make_frame(self, args)
        co_flags = self.func_code.co_flags
        if co_flags & CodeFlag.GENERATOR:
            return Generator(frame, self._interpreter)
        elif co_flags & CodeFlag.COROUTINE:
            return Coroutine(frame, self._interpreter)
        return self._interpreter.eval_frame(frame)


class Generator:

    def __init__(self, frame, interpreter) -> None:
        self.frame = frame
        self.interpreter = interpreter
        self.started = False
        self.finished = False

    def __iter__(self) -> 'Generator':
        return self

    def __next__(self) -> Any:
        return self.send(None)

    def send(self, value: Any) -> Any:
        if not self.started and value is not None:
            raise TypeError("Can't send non-None value to a just-started generator")
        self.frame.push(value)
        self.started = True
        retval = self.interpreter.eval_frame(self.frame)
        if self.frame.returned():
            raise StopIteration(retval)
        return retval


class Coroutine(Generator, CoroutineBase):

    def __await__(self):
        return self

    def throw(self):
        pass
