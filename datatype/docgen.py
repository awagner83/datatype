"""Generate docblock text for datatype definitions."""

from itertools import ifilter
from pprint import pformat


def add_docs(fn, datatype):
    """Add datatype definition to function docblock."""
    min_indent = getindent(fn.__doc__)
    fn.__doc__ = '%s\n\n%s' % (
            fn.__doc__,
            indent(gendocs(datatype, 80 - min_indent), min_indent)
        )


def gendocs(datatype, width=80):
    width -= 4
    return ('Return datatype:\n%s'
            % indent(pformat(datatype, width=width)))


def indent(string, indent_level=4):
    """Indent each line by `indent_level` of spaces."""
    return '\n'.join('%s%s' % (' '*indent_level, x) for x in
            string.splitlines())


def getindent(string):
    try:
        indent_levels = (nspaces(x) for x in string.splitlines() if x)
        return min(ifilter(lambda x: x != 0, indent_levels)) or 0
    except (AttributeError, ValueError):
        # Things that don't look like strings and strings with no
        # indentation should report indentation of 0
        return 0


def nspaces(line):
    for idx, char in enumerate(line):
        if char != ' ':
            return idx

