"""Console module for getting geometry or printing in color."""

import os
from fcntl import ioctl
from struct import unpack
from termios import TIOCGWINSZ

import six


def get_terminal_size():
    """Return terminal size."""

    def ioctl_GWINSZ(fd):
        try:
            cr = unpack('hh', ioctl(fd, TIOCGWINSZ, '1234'))
        except:
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            with os.open(os.ctermid(), os.O_RDONLY) as fd:
                cr = ioctl_GWINSZ(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.env['LINES'], os.env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

CONSOLE_FONT_ATTRIBUTE = {"NORMAL": 0,
                          "BOLD": 1,
                          "UNDERSCORE": 4,
                          "REVERSED": 7,
                          "DEFAULT": -1}

CONSOLE_FONT_FG_COLOR = {"BLACK": 30,
                         "RED": 31,
                         "GREEN": 32,
                         "YELLOW": 33,
                         "BLUE": 34,
                         "MAGENTA": 35,
                         "CYAN": 36,
                         "WHITE": 37,
                         "DEFAULT": -1}

CONSOLE_FONT_BG_COLOR = {"BLACK": 40,
                         "RED": 41,
                         "GREEN": 42,
                         "YELLOW": 43,
                         "BLUE": 44,
                         "MAGENTA": 45,
                         "CYAN": 46,
                         "WHITE": 47,
                         "DEFAULT": -1}


def string_in_color(font_attr, bg_color, fg_color, *args):
    """Return a colorful string."""

    formatter = []
    if font_attr != CONSOLE_FONT_ATTRIBUTE["DEFAULT"]:
        formatter.append(str(font_attr))
    if bg_color != CONSOLE_FONT_BG_COLOR["DEFAULT"]:
        formatter.append(str(bg_color))
    if fg_color != CONSOLE_FONT_FG_COLOR["DEFAULT"]:
        formatter.append(str(fg_color))
    return "\033[%sm%s\033[0m" % (';'.join(formatter), ' '.join(args))


def print_in_color(font_attr, bg_color, fg_color, *args):
    """Print in color."""

    formatter = []
    if font_attr != CONSOLE_FONT_ATTRIBUTE["DEFAULT"]:
        formatter.append(str(font_attr))
    if bg_color != CONSOLE_FONT_BG_COLOR["DEFAULT"]:
        formatter.append(str(bg_color))
    if fg_color != CONSOLE_FONT_FG_COLOR["DEFAULT"]:
        formatter.append(str(fg_color))
    six.print_("\033[%sm%s\033[0m" % (';'.join(formatter), ' '.join(args)), end='')
