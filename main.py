import sys

from src.interpreter import Interpreter


def main():
    assert len(sys.argv) >= 2
    with open(sys.argv[1], 'r') as infile:
        source = infile.read()

    code = compile(source, sys.argv[1], 'exec')
    Interpreter().run(code)


if __name__ == '__main__':
    main()
