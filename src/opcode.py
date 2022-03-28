import operator


class OpCode:
    POP_TOP = 1
    ROT_TWO = 2
    ROT_THREE = 3
    DUP_TOP = 4
    DUP_TOP_TWO = 5
    ROT_FOUR = 6
    NOP = 9
    UNARY_POSITIVE = 10
    UNARY_NEGATIVE = 11
    UNARY_NOT = 12
    UNARY_INVERT = 15
    BINARY_MATRIX_MULTIPLY = 16
    INPLACE_MATRIX_MULTIPLY = 17
    BINARY_POWER = 19
    BINARY_MULTIPLY = 20
    BINARY_MODULO = 22
    BINARY_ADD = 23
    BINARY_SUBTRACT = 24
    BINARY_SUBSCR = 25
    BINARY_FLOOR_DIVIDE = 26
    BINARY_TRUE_DIVIDE = 27
    INPLACE_FLOOR_DIVIDE = 28
    INPLACE_TRUE_DIVIDE = 29
    GET_LEN = 30
    MATCH_MAPPING = 31
    MATCH_SEQUENCE = 32
    MATCH_KEYS = 33
    COPY_DICT_WITHOUT_KEYS = 34
    WITH_EXCEPT_START = 49
    GET_AITER = 50
    GET_ANEXT = 51
    BEFORE_ASYNC_WITH = 52
    END_ASYNC_FOR = 54
    INPLACE_ADD = 55
    INPLACE_SUBTRACT = 56
    INPLACE_MULTIPLY = 57
    INPLACE_MODULO = 59
    STORE_SUBSCR = 60
    DELETE_SUBSCR = 61
    BINARY_LSHIFT = 62
    BINARY_RSHIFT = 63
    BINARY_AND = 64
    BINARY_XOR = 65
    BINARY_OR = 66
    INPLACE_POWER = 67
    GET_ITER = 68
    GET_YIELD_FROM_ITER = 69
    PRINT_EXPR = 70
    LOAD_BUILD_CLASS = 71
    YIELD_FROM = 72
    GET_AWAITABLE = 73
    LOAD_ASSERTION_ERROR = 74
    INPLACE_LSHIFT = 75
    INPLACE_RSHIFT = 76
    INPLACE_AND = 77
    INPLACE_XOR = 78
    INPLACE_OR = 79
    LIST_TO_TUPLE = 82
    RETURN_VALUE = 83
    IMPORT_STAR = 84
    SETUP_ANNOTATIONS = 85
    YIELD_VALUE = 86
    POP_BLOCK = 87
    POP_EXCEPT = 89
    STORE_NAME = 90
    DELETE_NAME = 91
    UNPACK_SEQUENCE = 92
    FOR_ITER = 93
    UNPACK_EX = 94
    STORE_ATTR = 95
    DELETE_ATTR = 96
    STORE_GLOBAL = 97
    DELETE_GLOBAL = 98
    ROT_N = 99
    LOAD_CONST = 100
    LOAD_NAME = 101
    BUILD_TUPLE = 102
    BUILD_LIST = 103
    BUILD_SET = 104
    BUILD_MAP = 105
    LOAD_ATTR = 106
    COMPARE_OP = 107
    IMPORT_NAME = 108
    IMPORT_FROM = 109
    JUMP_FORWARD = 110
    JUMP_IF_FALSE_OR_POP = 111
    JUMP_IF_TRUE_OR_POP = 112
    JUMP_ABSOLUTE = 113
    POP_JUMP_IF_FALSE = 114
    POP_JUMP_IF_TRUE = 115
    LOAD_GLOBAL = 116
    IS_OP = 117
    CONTAINS_OP = 118
    RERAISE = 119
    JUMP_IF_NOT_EXC_MATCH = 121
    SETUP_FINALLY = 122
    LOAD_FAST = 124
    STORE_FAST = 125
    DELETE_FAST = 126
    GEN_START = 129
    RAISE_VARARGS = 130
    CALL_FUNCTION = 131
    MAKE_FUNCTION = 132
    BUILD_SLICE = 133
    LOAD_CLOSURE = 135
    LOAD_DEREF = 136
    STORE_DEREF = 137
    DELETE_DEREF = 138
    CALL_FUNCTION_KW = 141
    CALL_FUNCTION_EX = 142
    SETUP_WITH = 143
    EXTENDED_ARG = 144
    LIST_APPEND = 145
    SET_ADD = 146
    MAP_ADD = 147
    LOAD_CLASSDEREF = 148
    MATCH_CLASS = 152
    SETUP_ASYNC_WITH = 154
    FORMAT_VALUE = 155
    BUILD_CONST_KEY_MAP = 156
    BUILD_STRING = 157
    LOAD_METHOD = 160
    CALL_METHOD = 161
    LIST_EXTEND = 162
    SET_UPDATE = 163
    DICT_MERGE = 164
    DICT_UPDATE = 165


BINARY_MAP = {
    OpCode.BINARY_MATRIX_MULTIPLY: operator.matmul,
    OpCode.BINARY_POWER: operator.pow,
    OpCode.BINARY_MULTIPLY: operator.mul,
    OpCode.BINARY_MODULO: operator.mod,
    OpCode.BINARY_ADD: operator.add,
    OpCode.BINARY_SUBTRACT: operator.sub,
    OpCode.BINARY_FLOOR_DIVIDE: operator.floordiv,
    OpCode.BINARY_TRUE_DIVIDE: operator.truediv,
    OpCode.BINARY_LSHIFT: operator.lshift,
    OpCode.BINARY_RSHIFT: operator.rshift,
    OpCode.BINARY_AND: operator.and_,
    OpCode.BINARY_XOR: operator.xor,
    OpCode.BINARY_OR: operator.or_,
}

UNARY_MAP = {
    OpCode.UNARY_POSITIVE: operator.pos,
    OpCode.UNARY_NEGATIVE: operator.neg,
    OpCode.UNARY_INVERT: operator.inv,
    OpCode.UNARY_NOT: operator.not_,
}

INPLACE_MAP = {
    OpCode.INPLACE_MATRIX_MULTIPLY: operator.imatmul,
    OpCode.INPLACE_FLOOR_DIVIDE: operator.ifloordiv,
    OpCode.INPLACE_TRUE_DIVIDE: operator.itruediv,
    OpCode.INPLACE_ADD: operator.iadd,
    OpCode.INPLACE_SUBTRACT: operator.isub,
    OpCode.INPLACE_MULTIPLY: operator.imul,
    OpCode.INPLACE_MODULO: operator.imod,
    OpCode.INPLACE_POWER: operator.ipow,
    OpCode.INPLACE_LSHIFT: operator.ilshift,
    OpCode.INPLACE_RSHIFT: operator.irshift,
    OpCode.INPLACE_AND: operator.iand,
    OpCode.INPLACE_XOR: operator.ixor,
    OpCode.INPLACE_OR: operator.ior,
}

BINARY_OPERATOR = BINARY_MAP | INPLACE_MAP


class CompareOp:
    LESS = 0
    LESS_EQUAL = 1
    EQUAL = 2
    NOT_EQUAL = 3
    GREATER = 4
    GREATER_EQUAL = 5
    IN = 6
    NOT_IN = 7
    IS = 8
    IS_NOT = 9
    EXC_MATCH = 10


COMPARE_MAP = {
    CompareOp.LESS: operator.lt,
    CompareOp.LESS_EQUAL: operator.le,
    CompareOp.EQUAL: operator.eq,
    CompareOp.NOT_EQUAL: operator.ne,
    CompareOp.GREATER: operator.gt,
    CompareOp.GREATER_EQUAL: operator.ge,
    # CompareOp.IN: operator.contains,
    # CompareOp.NOT_IN: lambda x, y: x not in y,
    # CompareOp.IS: operator.is_,
    # CompareOp.IS_NOT: operator.is_not,
    # CompareOp.EXC_MATCH: operator.less,
}
