"""Datatype validation module.

Provides:
    `failures`: Returns list of a values validation failures.
    `is_valid`: Returns boolean value representing validity of a value.
"""

from collections import defaultdict
from functools import partial


class BadDatatypeDefinitionError(Exception):
    """Raised when trying to validate with a bad datatype definition."""


def is_valid(datatype, value):
    """Return boolean representing validity of `value` against `datatype`."""
    return not failures(datatype, value)


def failures(datatype, value, path=''):
    """Return list of failures (if any) validating `value` again `datatype`.

    Params:
        `datatype`: Datatype to validate value against.  See README.markdown
            for examples.
        `value`: Value to validate
        `path`: Used internally for location of failures.

    Example:
        >>> failures('int', 'foo')
        ['expected int, got str']
    """
    dt_type = type(datatype)
    val_type = type(value)
    fails = []

    # Primitives Validation
    if dt_type == str:
        datatype, options = _parse_primitive(datatype)
        req_type = _primitives[datatype]
        if value is None:
            if 'nullable' not in options:
                fails.append(_failure(path,
                    'unexpected null for non-nullable type'))
        elif val_type not in req_type:
            fails.append(_failure(path,
                'expected %s, got %s',
                req_type[0].__name__, val_type.__name__
            ))

    # Object Validation
    elif dt_type == dict:
        fails.extend(_validate_dictionary(datatype, value, path))

    # List Validation
    elif dt_type == list and len(datatype) == 1:
        subtype = datatype[0]
        for idx, subval in enumerate(value):
            subpath = _joinpaths(path, '[%d]' % idx)
            fails.extend(failures(subtype, subval, subpath))

    # Tuple Validation
    elif dt_type == list and len(datatype) > 1:
        for idx, subtype in enumerate(datatype):
            subpath = _joinpaths(path, '[%d]' % idx)
            try:
                fails.extend(failures(subtype, value[idx], subpath))
            except IndexError:
                fails.append(_failure(path,
                    'missing required value at index %d', idx))

        # Check for unexpected items
        fails.extend(_failure(path, 'unexpected value at index %d' % x)
                for x in xrange(len(datatype), len(value)))

    # The great undefined!
    else:
        raise BadDatatypeDefinitionError(datatype)

    return fails


def _validate_dictionary(datatype, value, path):
    val_type = type(value)

    if val_type not in (dict, defaultdict):
        return [_failure(path, 'expected dict, got %s', val_type.__name__)]

    fails = []
    wildcard = datatype.get('_any_', None)
    all_properties = set()
    for key, subtype in datatype.iteritems():
        if key == '_any_':
            continue
        key, options = _parse_dict_key(key)
        all_properties.add(key)
        subpath = _joinpaths(path, key, '.')
        try:
            fails.extend(failures(subtype, value[key], subpath))
        except (KeyError):
            if 'optional' not in options:
                fails.append(_failure(path,
                    'missing required property: "%s"', key
                ))

    if wildcard:
        # validate wildcard items
        for key, subvalue in value.iteritems():
            subpath = _joinpaths(path, key, '.')
            fails.extend(failures(wildcard, subvalue, subpath))
    else:
        # check for unexpected properties/keys
        fails.extend(_failure(path, 'unexpected property "%s"', x)
                     for x in set(value.keys()) - all_properties)

    return fails


_primitives = {
        'int':   (int,),
        'float': (float,),
        'str':   (str, unicode),
        'bool':  (bool,)
    }

def _joinpaths(p1, p2, delim=None):
    return '%s%s%s' % (p1, delim, p2) if delim and p1 else '%s%s' % (p1, p2)


def _failure(path, error, *replacements):
    error = error % replacements
    return "%s: %s" % (path, error) if path else error


def _parse_name_options(key, possible_options):
    """Pull dictionary key options from key and return both as tuple.

    Example:
        >>> _parse_name_options("optional foo", ['optional'])
        ('foo', ['optional'])
    """
    key_words = iter(key.split(' '))
    options = []
    for word in key_words:
        if word in possible_options and word not in options:
            options.append(word)
        else:
            return (' '.join([word] + list(key_words)), options)


_parse_dict_key = partial(_parse_name_options, possible_options=['optional'])
_parse_primitive = partial(_parse_name_options, possible_options=['nullable'])

