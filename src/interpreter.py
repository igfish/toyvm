import dis
from types import CodeType, CoroutineType
from typing import Any

from src.frame import Frame, FrameState
from src.function import Cell, Function, Generator
from src.opcode import BINARY_OPERATOR, COMPARE_MAP, UNARY_MAP, OpCode

OPMAP = {v: k for k, v in dis.opmap.items()}


class Interpreter:

    def __init__(self):
        self.builtins = __builtins__.copy()
        self.frame: Frame = None
        self.return_value: Any = None
        self.extended_arg = 0

    def build_class(self, func: Function, name: str, *bases: Any, metaclass: Any = type, **kwargs: Any):
        assert isinstance(func, Function)
        frame = self.make_frame(func, ())
        self.eval_frame(frame)
        kwargs.update(frame.locals)
        return metaclass(name, bases, kwargs)

    def make_frame(self, func: Function, args: tuple[Any]):
        return Frame(
            func.code, self.frame, func.globals, args,
            func.defaults, self.frame.builtins, func.closure)

    def eval_generator(self, gtor: Generator):
        pass

    def eval_frame(self, frame: Frame):
        self.frame = frame
        self.frame.state = FrameState.EXECUTING
        while self.frame.can_advance():
            opcode, oparg = self.frame.next_instr()
            # print(f'{OPMAP[opcode]}  {oparg}')
            oparg |= (self.extended_arg << 8)
            self.extended_arg = 0
            if opcode in BINARY_OPERATOR:
                operator = BINARY_OPERATOR[opcode]
                a, b = self.frame.pop(), self.frame.pop()
                self.frame.push(operator(b, a))
                continue
            elif opcode in UNARY_MAP:
                operator = UNARY_MAP[opcode]
                self.frame.push(operator(self.frame.pop()))
                continue
            match opcode:
                case OpCode.NOP:
                    pass
                case OpCode.POP_TOP:
                    self.frame.pop()
                case OpCode.DUP_TOP:
                    self.frame.push(self.frame.top())
                case OpCode.DUP_TOP_TWO:
                    # 未找到例子
                    pass
                case OpCode.ROT_TWO:
                    # 交换两个最顶层的堆栈项
                    a, b = self.frame.pop(), self.frame.pop()
                    self.frame.push(a)
                    self.frame.push(b)
                case OpCode.ROT_THREE:
                    a, b, c = self.frame.pop(), self.frame.pop(), self.frame.pop()
                    # 将第二个和第三个堆栈项向上提升一个位置，顶项移动到位置三
                    self.frame.push(a)
                    self.frame.push(c)
                    self.frame.push(b)
                case OpCode.ROT_FOUR:
                    # 将第二个、第三个和第四个堆栈项向上提升一个位置，将顶项移动到第四个位置
                    # 未找到例子
                    pass
                case OpCode.GET_LEN:
                    # 未找到例子
                    pass
                case OpCode.BINARY_SUBSCR:
                    index = self.frame.pop()
                    obj = self.frame.pop()
                    self.frame.push(obj[index])
                case OpCode.STORE_SUBSCR:
                    index = self.frame.pop()
                    obj = self.frame.pop()
                    obj[index] = self.frame.pop()
                case OpCode.DELETE_SUBSCR:
                    index = self.frame.pop()
                    obj = self.frame.pop()
                    del obj[index]
                case OpCode.GET_ITER:
                    self.frame.push(iter(self.frame.pop()))
                case OpCode.RETURN_VALUE:
                    return_value = self.frame.pop()
                    break
                case OpCode.POP_BLOCK:
                    raise NotImplementedError
                case OpCode.STORE_NAME:
                    name = self.frame.names[oparg]
                    self.frame.locals[name] = self.frame.pop()
                case OpCode.UNPACK_SEQUENCE:
                    sequence = self.frame.pop()
                    assert len(sequence) == oparg
                    for i in range(oparg - 1, -1, -1):
                        self.frame.push(sequence[i])
                case OpCode.UNPACK_EX:
                    leftcount = oparg & 0xFF
                    rightcount = oparg >> 8
                    assert rightcount == 2
                    assert leftcount == 3
                    sequence = self.frame.pop()
                    for i in range(len(sequence) - 1, len(sequence) - rightcount - 1, -1):
                        self.frame.push(sequence[i])
                    self.frame.push([sequence[i] for i in range(leftcount, len(sequence) - rightcount)])
                    for i in range(leftcount - 1, -1, -1):
                        self.frame.push(sequence[i])
                case OpCode.DELETE_NAME:
                    name = self.frame.names[oparg]
                    del self.frame.locals[name]
                case OpCode.FOR_ITER:
                    itor = self.frame.top()
                    try:
                        self.frame.push(next(itor))
                    except StopIteration:
                        self.frame.pop()
                        self.frame.jump_forward(oparg << 1)
                case OpCode.STORE_GLOBAL:
                    name = self.frame.names[oparg]
                    self.frame.globals[name] = self.frame.pop()
                case OpCode.DELETE_GLOBAL:
                    name = self.frame.names[oparg]
                    del self.frame.globals[name]
                case OpCode.LOAD_CONST:
                    self.frame.push(self.frame.consts[oparg])
                case OpCode.LOAD_NAME:
                    name = self.frame.names[oparg]
                    has_find = False
                    for namespace in [self.frame.locals, self.frame.globals, self.frame.builtins]:
                        if name in namespace:
                            self.frame.push(namespace[name])
                            has_find = True
                            break
                    if not has_find:
                        raise RuntimeError(f'{name} not find')
                case OpCode.LOAD_CLOSURE:
                    self.frame.push(self.frame.closure[oparg])
                case OpCode.LOAD_DEREF:
                    cell = self.frame.closure[oparg]
                    assert isinstance(cell, Cell)
                    self.frame.push(cell.value)
                case OpCode.STORE_DEREF:
                    value = self.frame.pop()
                    self.frame.closure[oparg] = Cell(value)
                case OpCode.BUILD_TUPLE:
                    tp = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        tp[i] = self.frame.pop()
                    self.frame.push(tuple(tp))
                case OpCode.BUILD_LIST:
                    lst = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        lst[i] = self.frame.pop()
                    self.frame.push(lst)
                case OpCode.LIST_APPEND:
                    value = self.frame.pop()
                    lst = self.frame.top(oparg)
                    assert isinstance(lst, list)
                    lst.append(value)
                case OpCode.LIST_EXTEND:
                    iterables = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        iterables[i] = self.frame.pop()
                    lst = self.frame.top()
                    assert isinstance(lst, list)
                    for _iterable in iterables:
                        lst.extend(_iterable)
                case OpCode.BUILD_MAP:
                    keys = [... for _ in range(oparg)]
                    values = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        values[i] = self.frame.pop()
                        keys[i] = self.frame.pop()
                    self.frame.push(dict(zip(keys, values)))
                case OpCode.BUILD_CONST_KEY_MAP:
                    keys = self.frame.pop()
                    values = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        values[i] = self.frame.pop()
                    self.frame.push(dict(zip(keys, values)))
                case OpCode.DICT_MERGE:
                    d1, d2 = self.frame.pop(), self.frame.pop()
                    for k in d1.keys():
                        assert k not in d2
                    self.frame.push({**d2, **d1})
                case OpCode.DICT_UPDATE:
                    d1, d2 = self.frame.pop(), self.frame.pop()
                    self.frame.push({**d2, **d1})
                case OpCode.LOAD_ATTR:
                    name = self.frame.names[oparg]
                    obj = self.frame.pop()
                    self.frame.push(getattr(obj, name))
                case OpCode.STORE_ATTR:
                    obj = self.frame.pop()
                    attr = self.frame.pop()
                    setattr(obj, self.frame.names[oparg], attr)
                case OpCode.CALL_METHOD:
                    args = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        args[i] = self.frame.pop()
                    func = self.frame.pop()
                    assert callable(func)
                    self.frame.push(func(*args))
                case OpCode.LOAD_METHOD:
                    name = self.frame.names[oparg]
                    obj = self.frame.pop()
                    self.frame.push(getattr(obj, name))
                case OpCode.COMPARE_OP:
                    a, b = self.frame.pop(), self.frame.pop()
                    self.frame.push(COMPARE_MAP[oparg](b, a))
                case OpCode.IS_OP:
                    a, b = self.frame.pop(), self.frame.pop()
                    self.frame.push(b is a if oparg == 0 else b is not a)
                case OpCode.CONTAINS_OP:
                    a, b = self.frame.pop(), self.frame.pop()
                    self.frame.push(b in a if oparg == 0 else b not in a)
                case OpCode.JUMP_FORWARD:
                    self.frame.jump_forward(oparg << 1)
                case OpCode.JUMP_ABSOLUTE:
                    self.frame.jump_to(oparg << 1)
                case OpCode.POP_JUMP_IF_FALSE:
                    not_jump = self.frame.pop()
                    assert isinstance(not_jump, bool)
                    if not not_jump:
                        # 指令编号必是偶数，节省内存
                        self.frame.jump_to(oparg << 1)
                case OpCode.POP_JUMP_IF_TRUE:
                    jump = self.frame.pop()
                    assert isinstance(jump, bool)
                    if jump:
                        self.frame.jump_to(oparg << 1)
                case OpCode.LOAD_GLOBAL:
                    name = self.frame.names[oparg]
                    has_find = False
                    for namespace in [self.frame.globals, self.frame.builtins]:
                        if name in namespace:
                            self.frame.push(namespace[name])
                            has_find = True
                            break
                    if not has_find:
                        raise NameError(f'name {repr(name)} is not defined')
                case OpCode.BUILD_SET:
                    self.frame.push(set())
                case OpCode.SET_UPDATE:
                    iterables = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        iterables[i] = self.frame.pop()
                    s = self.frame.top()
                    s.update(*iterables)
                case OpCode.SET_ADD:
                    value = self.frame.pop()
                    s = self.frame.top(oparg)
                    assert isinstance(s, set)
                    s.add(value)
                case OpCode.LOAD_FAST:
                    self.frame.push(self.frame.fast_locals[oparg])
                case OpCode.STORE_FAST:
                    self.frame.fast_locals[oparg] = self.frame.pop()
                case OpCode.LOAD_BUILD_CLASS:
                    self.frame.push(self.build_class)
                case OpCode.MAKE_FUNCTION:
                    name = self.frame.pop()
                    code = self.frame.pop()
                    assert isinstance(code, CodeType)
                    if oparg & 0x08:  # 一个包含用于自由变量的单元的元组，生成一个闭包与函数相关联的代码
                        closure = self.frame.pop()
                    else:
                        closure = ()
                    if oparg & 0x01:  # 0x01 一个默认值的元组，用于按位置排序的仅限位置形参以及位置或关键字形参
                        defaults = self.frame.pop()
                    else:
                        defaults = ()
                    func = Function(name, code, self.frame.globals, defaults, closure, self)
                    self.frame.push(func)
                case OpCode.CALL_FUNCTION:
                    args = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        args[i] = self.frame.pop()
                    func = self.frame.pop()
                    assert callable(func)
                    self.frame.push(func(*args))
                case OpCode.CALL_FUNCTION_KW:  # *args **kwargs
                    argnames = self.frame.pop()
                    args = [... for _ in range(oparg)]
                    for i in range(oparg - 1, -1, -1):
                        args[i] = self.frame.pop()
                    func = self.frame.pop()
                    posargcount = oparg - len(argnames)
                    kwargs = dict(zip(argnames, args[posargcount:]))
                    assert callable(func)
                    self.frame.push(func(*args[:posargcount], **kwargs))
                case OpCode.CALL_FUNCTION_EX:
                    kwargs = self.frame.pop() if oparg == 1 else {}
                    posargs = self.frame.pop()
                    func = self.frame.pop()
                    assert callable(func)
                    self.frame.push(func(*posargs, **kwargs))
                case OpCode.MAP_ADD:
                    value, key = self.frame.pop(), self.frame.pop()
                    mp = self.frame.top(oparg)
                    assert isinstance(mp, dict)
                    mp[key] = value
                case OpCode.EXTENDED_ARG:
                    self.extended_arg = oparg
                case OpCode.GEN_START:
                    self.frame.pop()
                case OpCode.YIELD_VALUE:
                    # self.frame.state = FrameState.SUSPENDED
                    retval = self.frame.pop()
                    self.frame = self.frame.f_back
                    return retval
                case OpCode.GET_YIELD_FROM_ITER:
                    obj = self.frame.pop()
                    if isinstance(obj, Generator):
                        self.frame.push(obj)
                    else:
                        self.frame.push(iter(obj))
                case OpCode.YIELD_FROM:
                    value = self.frame.pop()
                    itor = self.frame.top()
                    try:
                        if isinstance(itor, (Generator, CoroutineType)):
                            retval = itor.send(value)
                        else:
                            retval = next(itor)
                    except StopIteration as ex:
                        self.frame.pop()
                        self.frame.push(ex.value)
                    else:
                        self.frame.jump_forward(-2)
                        self.frame = self.frame.f_back
                        return retval
                case OpCode.IMPORT_NAME:
                    name = self.frame.names[oparg]
                    fromlist, level = self.frame.pop(), self.frame.pop()
                    self.frame.push(__import__(name, self.frame.globals, self.frame.locals, fromlist, level))
                case OpCode.IMPORT_FROM:
                    name = self.frame.names[oparg]
                    self.frame.push(getattr(self.frame.top(), name))
                case OpCode.IMPORT_STAR:
                    module = self.frame.pop()
                    for k, v in module.__dict__.items():
                        if not k.startswith('_'):
                            self.frame.locals[k] = v
                case OpCode.GET_AWAITABLE:
                    pass
                case _:
                    raise RuntimeError('Unrecognized opcode: %s' % opcode)

        self.frame.state = FrameState.RETURNED
        self.frame = self.frame.f_back
        return return_value

    def run(self, code: CodeType):
        frame = Frame(code, builtins=self.builtins)
        self.eval_frame(frame)
