

class BadDatatypeDefinitionError(Exception):
    """Raised when trying to validate with a bad datatype definition."""


def failures(datatype, value, path=''):
    dt_type = type(datatype)
    fails = []

    # Primitives Validation
    if dt_type == str:
        val_type = type(value)
        req_type = _primitives[datatype]
        if val_type != req_type:
            fails.append(_failure(path,
                'expected %s, got %s',
                req_type.__name__, val_type.__name__
            ))

    # Object Validation
    elif dt_type == dict:
        for key, subtype in datatype.iteritems():
            key, options = _parse_dict_key(key)
            subpath = _joinpaths(path, key, '.')
            try:
                fails.extend(failures(subtype, value[key], subpath))
            except (KeyError):
                if 'optional' not in options:
                    fails.append(_failure(path,
                        'missing required property: "%s"', key
                    ))

    # List Validation
    elif dt_type == list:
        raise NotImplementedError

    # The great undefined!
    else:
        raise BadDatatypeDefinitionError(datatype)

    return fails


def is_valid(datatype, value):
    return not failures(datatype, value)


_primitives = {
        'int':   int,
        'float': float,
        'str':   str,
        'bool':  bool
    }

def _joinpaths(p1, p2, delim=None):
    return ''.join((p1, delim, p2)) if delim and p1 else ''.join((p1, p2))


def _failure(path, error, *replacements):
    error = error % replacements
    return "%s: %s" % (path, error) if path else error


_dict_key_options = [
        'optional'
    ]


def _parse_dict_key(key):
    """Pull dictionary key options from key and return both as tuple.

    Example:
        >>> _parse_dict_key("optional foo")
        ('foo', ['optional'])
    """
    key_words = iter(key.split(' '))
    options = []
    for word in key_words:
        if word in _dict_key_options and word not in options:
            options.append(word)
        else:
            return (' '.join([word] + list(key_words)), options)


