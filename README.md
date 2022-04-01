# ToyVM
[中文](README_CN.md)[English](README.md)
A Python virtual machine written in Python.
Compatible with python3.10 instructions.
The runtime environment requires Python version 3.10.

## Usage
```shell
python3.10 main.py examples/basic.py
```

The VM terminal UI is enabled:
```shell
python3.10 main.py examples/yield_producer_consumer.py --enable-vis --pause=0.5
```

Running simple tests:
```
./run_tests.sh
```

Completed (partially completed) instructions:
- [x] POP_TOP
- [x] ROT_TWO
- [x] ROT_THREE
- [x] DUP_TOP
- [x] NOP
- [x] UNARY_POSITIVE
- [x] UNARY_NEGATIVE
- [x] UNARY_NOT
- [x] UNARY_INVERT
- [x] BINARY_MATRIX_MULTIPLY
- [x] INPLACE_MATRIX_MULTIPLY
- [x] BINARY_POWER
- [x] BINARY_MULTIPLY
- [x] BINARY_MODULO
- [x] BINARY_ADD
- [x] BINARY_SUBTRACT
- [x] BINARY_SUBSCR
- [x] BINARY_FLOOR_DIVIDE
- [x] BINARY_TRUE_DIVIDE
- [x] INPLACE_FLOOR_DIVIDE
- [x] INPLACE_TRUE_DIVIDE
- [x] INPLACE_ADD
- [x] INPLACE_SUBTRACT
- [x] INPLACE_MULTIPLY
- [x] INPLACE_MODULO
- [x] STORE_SUBSCR
- [x] DELETE_SUBSCR
- [x] BINARY_LSHIFT
- [x] BINARY_RSHIFT
- [x] BINARY_AND
- [x] BINARY_XOR
- [x] BINARY_OR
- [x] INPLACE_POWER
- [x] GET_ITER
- [x] GET_YIELD_FROM_ITER
- [x] LOAD_BUILD_CLASS
- [x] YIELD_FROM
- [x] GET_AWAITABLE
- [x] INPLACE_LSHIFT
- [x] INPLACE_RSHIFT
- [x] INPLACE_AND
- [x] INPLACE_XOR
- [x] INPLACE_OR
- [x] RETURN_VALUE
- [x] IMPORT_STAR
- [x] YIELD_VALUE
- [x] STORE_NAME
- [x] DELETE_NAME
- [x] UNPACK_SEQUENCE
- [x] FOR_ITER
- [x] UNPACK_EX
- [x] STORE_ATTR
- [x] STORE_GLOBAL
- [x] DELETE_GLOBAL
- [x] LOAD_CONST
- [x] LOAD_NAME
- [x] BUILD_TUPLE
- [x] BUILD_LIST
- [x] BUILD_SET
- [x] BUILD_MAP
- [x] LOAD_ATTR
- [x] COMPARE_OP
- [x] IMPORT_NAME
- [x] IMPORT_FROM
- [x] JUMP_ABSOLUTE
- [x] POP_JUMP_IF_FALSE
- [x] POP_JUMP_IF_TRUE
- [x] LOAD_GLOBAL
- [x] IS_OP
- [x] CONTAINS_OP
- [x] LOAD_FAST
- [x] STORE_FAST
- [x] GEN_START
- [x] CALL_FUNCTION
- [x] MAKE_FUNCTION
- [x] LOAD_CLOSURE
- [x] LOAD_DEREF
- [x] STORE_DEREF
- [x] CALL_FUNCTION_KW
- [x] CALL_FUNCTION_EX
- [x] EXTENDED_ARG
- [x] LIST_APPEND
- [x] SET_ADD
- [x] MAP_ADD
- [x] BUILD_CONST_KEY_MAP
- [x] LOAD_METHOD
- [x] CALL_METHOD
- [x] LIST_EXTEND
- [x] SET_UPDATE
- [x] DICT_MERGE

Unimplemented instructions:
- [ ] DUP_TOP_TWO
- [ ] ROT_FOUR
- [ ] GET_LEN
- [ ] MATCH_MAPPING
- [ ] MATCH_SEQUENCE
- [ ] MATCH_KEYS
- [ ] COPY_DICT_WITHOUT_KEYS
- [ ] WITH_EXCEPT_START
- [ ] GET_AITER
- [ ] GET_ANEXT
- [ ] BEFORE_ASYNC_WITH
- [ ] END_ASYNC_FOR
- [ ] PRINT_EXPR
- [ ] LOAD_ASSERTION_ERROR
- [ ] LIST_TO_TUPLE
- [ ] SETUP_ANNOTATIONS
- [ ] POP_BLOCK
- [ ] POP_EXCEPT
- [ ] DELETE_ATTR
- [ ] ROT_N
- [ ] JUMP_FORWARD
- [ ] JUMP_IF_FALSE_OR_POP
- [ ] JUMP_IF_TRUE_OR_POP
- [ ] RERAISE
- [ ] JUMP_IF_NOT_EXC_MATCH
- [ ] SETUP_FINALLY
- [ ] DELETE_FAST
- [ ] RAISE_VARARGS
- [ ] BUILD_SLICE
- [ ] DELETE_DEREF
- [ ] SETUP_WITH
- [ ] LOAD_CLASSDEREF
- [ ] MATCH_CLASS
- [ ] SETUP_ASYNC_WITH
- [ ] FORMAT_VALUE
- [ ] BUILD_STRING
- [ ] DICT_UPDATE