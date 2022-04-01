from dataclasses import dataclass
from types import CodeType
from typing import Any

from src.function import Cell, CodeFlag


@dataclass
class Block:
    type: int
    target: int
    level: int


class FrameState:
    CREATED = -2
    SUSPENDED = -1
    EXECUTING = 0
    RETURNED = 1
    UNWINDING = 2
    RAISED = 3
    CLEARED = 4


class Frame:

    def __init__(self, code: CodeType,
                 back: 'Frame' = None,
                 globals: dict[str, Any] = None,
                 args: tuple[Any] = (),
                 defaults: tuple[Any] = (),
                 builtins: dict[str, Any] = None,
                 closure: tuple[Cell] = ()) -> None:
        self.f_back = back
        self.f_code = code
        self.f_builtins = builtins
        self.f_locals: dict[str, Any] = {}
        # First frame.
        self.f_globals = globals if globals is not None else self.f_locals
        self.f_stack: list[Any] = []
        self.f_loop_stack: list[Any] = []
        self.f_fast_locals = [*args, *defaults[len(args) - code.co_argcount + 1:]]
        if self.code.co_flags & CodeFlag.NEWLOCALS:
            for _ in range(len(self.code.co_varnames) - len(self.f_fast_locals)):
                self.f_fast_locals.append(...)
        self.f_closure = [... for _ in range(len(code.co_freevars) + len(code.co_cellvars))]
        assert len(closure) == len(code.co_freevars)
        for i, c in enumerate(closure):
            self.f_closure[i] = c
        for i, name in enumerate(code.co_cellvars, len(code.co_freevars)):
            if name in code.co_varnames:
                self.f_closure[i] = Cell(self.f_fast_locals[code.co_varnames.index(name)])
        self.f_lasti = 0
        self.f_state = FrameState.CREATED

    @property
    def code(self):
        return self.f_code

    @property
    def back(self):
        return self.f_back

    @property
    def builtins(self):
        return self.f_builtins

    @property
    def locals(self):
        return self.f_locals

    @property
    def globals(self):
        return self.f_globals

    @property
    def fast_locals(self):
        return self.f_fast_locals

    @property
    def consts(self):
        return self.f_code.co_consts

    @property
    def names(self):
        return self.f_code.co_names

    @property
    def argcount(self):
        return self.f_code.co_argcount

    @property
    def closure(self):
        return self.f_closure

    def top(self, n=1):
        return self.f_stack[-n]

    @property
    def stack(self):
        return self.f_stack

    @property
    def state(self):
        return self.f_state

    @state.setter
    def state(self, state: FrameState):
        self.f_state = state

    def pop(self):
        return self.f_stack.pop()

    def push(self, o: Any):
        return self.f_stack.append(o)

    def is_first_frame(self) -> bool:
        return self.f_back is None

    def jump_to(self, to: int):
        self.f_lasti = to

    def jump_forward(self, delta: int):
        self.f_lasti += delta

    def next_instr(self) -> tuple[int, int]:
        lasti = self.f_lasti
        self.f_lasti += 2
        return self.f_code.co_code[lasti:self.f_lasti]

    def can_advance(self) -> int:
        return self.f_lasti < len(self.f_code.co_code)

    def returned(self):
        return self.f_state == FrameState.RETURNED

    def __repr__(self):
        return '<Frame {}>'.format(repr(self.f_code.co_name))
