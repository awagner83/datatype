"""Datatype utility functions.  Used by datatype validation and coercion."""

from collections import defaultdict
from functools import partial
from itertools import count


class NewValue(object):
    """Returned from walk-callback when we want to replace the value."""

    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value


class Choice(object):
    """Datatype representing a choice between multiple datatypes."""

    def __init__(self, choices):
        self.choices = choices

    def __iter__(self):
        return iter(self.choices)

    def __eq__(self, other):
        return isinstance(other, Choice) and self.choices == other.choices

    def __repr__(self):
        return '<Choice of %s>' % self.choices

    def __str__(self):
        if len(self.choices) < 3:
            return ' or '.join(self.choices)
        else:
            return '%s, or %s' % (
                    ', '.join(self.choices[:-1]),
                    self.choices[-1]
                )


def dict_datatypes(datatype):
    default = datatype.get('_any_')
    datatypes = defaultdict(lambda: default)

    for key, val in datatype.iteritems():
        if isinstance(val, str):
            key, _ = parse_dict_key(key)
        else:
            key = key
        datatypes[key] = val

    return datatypes


def extract_named_types(datatype):
    """Walks the given datatype, removes the named-wrappers from around the
    types and returns a dictionary of names -> types as well as the cleaned
    datatype."""
    named_types = {}

    if datatype_type(datatype) == 'named':
        named_types[datatype['name']] = datatype['value']
        datatype = datatype['value']

    dt_type = type(datatype)
    if dt_type in (list, dict):
        generators = {
                list: lambda: enumerate(datatype),
                dict: lambda: datatype.iteritems(),
            }
        for key, subtype in generators[dt_type]():
            sub_named_types, subtype = extract_named_types(subtype)
            named_types.update(sub_named_types)
            datatype[key] = subtype

    return named_types, datatype


def walk(datatype, value, callback):
    """Walk the value and datatype with the given callback.

    Example callback: lambda path, datatype, actual, options: None"""
    named_types, datatype = extract_named_types(datatype)

    def _walk(datatype, value, callback, path='', options=None):
        options = options or []
        if isinstance(datatype, str):
            datatype, parsed_options = parse_primitive(datatype)
            options += parsed_options

        # Transform special types:
        dt_type = datatype_type(datatype)
        if dt_type == 'choice':
            datatype = Choice(datatype.get('choices'))
        elif dt_type == 'reference':
            datatype = named_types[datatype['name']]

        new_value = callback(path, datatype, value, options)

        # Are we replacing the value?
        if isinstance(new_value, NewValue):
            value = new_value.value

        # Walk lists and tuples
        if are_type(list, datatype, value):
            dt_len = len(datatype)
            mk_path = lambda i: joinpaths(path, '[%d]' % i)

            if dt_len == 1:   # list of `a`
                value = [_walk(datatype[0], v, callback, mk_path(i))
                         for i, v in enumerate(value)]
            elif dt_len > 1:  # tuple
                value = [_walk(d, v, callback, mk_path(i))
                         for i, d, v in zip(count(), datatype, value)]

        # Walk objects (dictionaries)
        elif are_type(dict, datatype, value):
            key_dts = dict_datatypes(datatype)
            mk_path = lambda k: joinpaths(path, k, '.')

            value = dict((k, _walk(key_dts[k], v, callback, mk_path(k)))
                for k, v in value.iteritems())

        return value
    return _walk(datatype, value, callback)


def are_type(type_, *vars_):
    return all(isinstance(v, type_) for v in vars_)


def datatype_type(datatype):
    default = 'type'
    if isinstance(datatype, dict):
        return datatype.get('_type_', default)
    else:
        return default


def joinpaths(p1, p2, delim=None):
    return '%s%s%s' % (p1, delim, p2) if delim and p1 else '%s%s' % (p1, p2)


def parse_name_options(key, possible_options):
    """Pull dictionary key options from key and return both as tuple.

    Example:
        >>> parse_name_options("optional foo", ['optional'])
        ('foo', ['optional'])
    """
    key_words = iter(key.split(' '))
    options = []
    for word in key_words:
        if word in possible_options and word not in options:
            options.append(word)
        else:
            return (' '.join([word] + list(key_words)), options)


parse_dict_key = partial(parse_name_options, possible_options=['optional'])
parse_primitive = partial(parse_name_options, possible_options=['nullable'])

