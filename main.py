import argparse
from cgitb import enable
import curses
from signal import pause
import sys

from src.interpreter import Interpreter
from src.visualize import draw


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-p',
                        '--pause',
                        action='store',
                        type=float,
                        default=0.05)
    parser.add_argument('--enable-vis',
                        action='store_true',
                        default=False)
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.filename, 'r') as infile:
        source = infile.read()

    code = compile(source, args.filename, 'exec')
    if args.enable_vis:
        drawer = curses.wrapper(draw)
        drawer.send(None)
        Interpreter(drawer, args.enable_vis, args.pause).run(code)
    else:
        Interpreter().run(code)


if __name__ == '__main__':
    main()
