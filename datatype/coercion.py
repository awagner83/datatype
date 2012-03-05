"""Datatype coercion.

Provides:
    `coerce_value`: Returns best attempt at coercing value to given type.
"""

__all__ = ['coerce_value']

from datatype.tools import NewValue, walk
from datatype.validation import primitives


coercable_types = reduce(list.__add__,
        (list(x) for x in primitives.itervalues()))

coerce_to = dict((k, v[0]) for k, v in primitives.iteritems())


def coerce_value(datatype, value):
    """Attempt to coerce value to requested datatype.

    Example:
    >>> coerce_value("int", "5")
    5
    """
    return walk(datatype, value, coerce_step)


def coerce_step(_, datatype, value, __):
    if type(datatype) == str and type(value) in coercable_types:
        return NewValue(coerce_to[datatype](value))

