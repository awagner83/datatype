"""Datatype 'language' definition.  Helpers for interactions with datatype's
special types."""


def typename(datatype):
    """Returns the type-name of the given datatype definition or chunk."""
    default = 'type'
    if isinstance(datatype, dict):
        return datatype.get('_type_', default)
    else:
        return default


def special_type(typename, **kwargs):
    """Construct a special type dictionary."""
    return dict(kwargs, _type_=typename)


def choice(*choices):
    """Returns a 'choice' dictionary of the given choices.

    Example:
        >>> choice('str', 'int')
        {'_type_': 'choice', 'choices': ['str', 'int']}
    """
    return special_type('choice', choices=list(choices))


def named(name, value):
    """Returns a 'named' dictionary for naming the given 'value' datatype.

    Example:
        >>> named('person', {'first_name': 'str'})
        {'_type_': 'named', 'name': 'person', 'value': {'first_name': 'str'}}
    """
    return special_type('named', name=name, value=value)


def reference(name):
    """Returns a 'reference' dictionary for the given named type.

    Example:
        >>> reference('person')
        {'_type_': 'reference', 'name': 'person'}
    """
    return special_type('reference', name=name)


def literal(value):
    """Returns a 'literal' dictionary.

    Example:
        >>> literal('foo')
        {'_type_': 'literal', 'value': 'foo'}
    """
    return special_type('literal', value=value)

