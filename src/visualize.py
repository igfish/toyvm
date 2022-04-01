import curses
import dis
import locale
from types import CodeType

from src.frame import Frame

locale.setlocale(locale.LC_ALL, '')


def get_repr(x):
    expr = repr(x)
    if len(expr) > 30:
        expr = '< {} object >'.format(type(x).__name__)
    return expr


def write_code(scr: curses.window, code: CodeType):
    _, width = scr.getmaxyx()
    scr.addstr(0, 0, '¯' * (width - 1))

    title = 'Toy Python Virtual Machine'
    title_length = len(title)
    titile_start_x = int((width // 2) - (title_length // 2) - title_length % 2)
    scr.addstr(1, titile_start_x, f'{title}\n')
    scr.addstr(2, 0, '_' * (width - 1))

    cursor_x, cursor_y = 3, 1
    co_name = 'Name: {}'.format(code.co_name)
    co_filename = 'Filename: {}'.format(code.co_filename)
    co_argcount = 'Argument count: {}'.format(code.co_argcount)
    co_kwonlyargcount = 'Kw-only arguments: {}'.format(code.co_kwonlyargcount)
    co_nlocals = 'Number of locals: {}'.format(code.co_nlocals)
    co_stacksize = 'Stack size: {}'.format(code.co_stacksize)
    co_flags = 'Flags: {}'.format(dis.pretty_flags(code.co_flags))
    co_consts = 'Constants: ({})'.format(', '.join([
        '{}: {}'.format(i, get_repr(x)) for i, x in enumerate(code.co_consts)
    ]))
    co_names = 'Names: ({})'.format(', '.join(
        ['{}: {}'.format(i, get_repr(x)) for i, x in enumerate(code.co_names)]))
    co_varnames = 'Variable names: ({})'.format(', '.join([
        '{}: {}'.format(i, get_repr(x)) for i, x in enumerate(code.co_varnames)
    ]))
    co_freevars = 'Free variables: ({})'.format(', '.join([
        '{}: {}'.format(i, get_repr(x)) for i, x in enumerate(code.co_freevars)
    ]))
    co_cellvars = 'Cell variables: ({})'.format(', '.join([
        '{}: {}'.format(i, get_repr(x)) for i, x in enumerate(code.co_cellvars)
    ]))
    divider = ','
    for x in (co_name, co_filename, co_argcount, co_kwonlyargcount, co_nlocals,
              co_stacksize, co_flags, co_consts, co_names, co_varnames,
              co_freevars, co_cellvars):
        if x is not co_cellvars:
            x += divider
        if cursor_y + len(x) > width:
            cursor_x += 1
            cursor_y = 1
        scr.addstr(cursor_x, cursor_y, x[:width - cursor_y])
        cursor_y += len(x) + 1
    for i in range(cursor_x + 2):
        scr.addstr(i, 0, '|')
        scr.addstr(i, width - 1, '|')
    return cursor_x + 1


def write_content(scr: curses.window, title: str, contents: list[str], curr: int = None, color=None):
    height, width = scr.getmaxyx()
    title_length = len(title)
    start_x = int((width // 2) - (title_length // 2) - title_length % 2)
    overline = '¯' * (width)
    underline = '_' * (width)
    scr.addstr(overline)
    scr.addstr(1, start_x, f'{title}\n')
    scr.addstr(underline)
    scr.addstr(height - 2, 0, underline)
    scr.addstr(1, 0, '|')

    if len(contents) > height - 4 and curr is not None:
        index = max(curr - (height - 4) // 2, 0)
    else:
        index = 0
    for i in range(3, height - 2):
        if i - 3 >= len(contents) or index >= len(contents):
            break
        content = contents[index][:width - 2]
        index += 1
        if curr is not None and i - 3 == curr and color is not None:
            scr.addstr(i, 1, content, color)
        else:
            scr.addstr(i, 1, content)

    for i in range(0, height - 1):
        scr.addstr(i, 0, '|')
    scr.addstr(1, width - 1, '|')
    for i in range(0, height - 1):
        scr.addstr(i, width - 1, '|')


def draw(stdscr: curses.window):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    color_blue = curses.color_pair(1)

    while True:
        # Initialization
        frame: Frame
        outputs: list[str]
        frame, outputs = yield
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        code_scr_height = write_code(stdscr, frame.code)
        body_height = height - code_scr_height - 4

        stack_scr = stdscr.derwin(body_height, width // 3, code_scr_height + 1, 0)
        instr_scr = stdscr.derwin(body_height, width // 3, code_scr_height + 1, width // 3)
        output_scr = stdscr.derwin(body_height, width // 3, code_scr_height + 1, width // 3 * 2)

        write_content(stack_scr, 'Stack', [str(x) for x in frame.stack])
        bytecode = dis.Bytecode(frame.code)

        instructions = []
        index = frame.f_lasti - 2
        for i, instr in enumerate(bytecode):
            if i * 2 == index:
                instructions.append('{:>2} ->{:<20} {}({})'.format(
                    instr.offset, instr.opname, instr.arg, instr.argval))
            else:
                instructions.append('{:>2}   {:<20} {}({})'.format(
                    instr.offset, instr.opname, instr.arg, instr.argval))
        write_content(
            instr_scr, 'Instuctions', instructions, curr=index // 2, color=color_blue)
        write_content(output_scr, 'Output', outputs, curr=len(outputs) - 1)

        stdscr.refresh()
