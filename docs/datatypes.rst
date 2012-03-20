Defining datatypes
==================

Datatype definitions are intended to look like the values they define, and are
themselves defined as anonymous datatypes.

For example, the following values::

    {'first_name': 'Bob', 'last_name': 'Smith'}
    {'first_name': 'John', 'last_name': 'Doe'}

are both valid instances of this datatype::

    {'first_name': 'str', 'last_name': 'str'}


Primitives
----------

Primitive types are defined as strings bearing the python constructor name.

- String: `"str"`
- Integer: `"int"`
- Float: `"float"`
- Boolean: `"bool"`

Primitive datatypes are, by default, not-nullable.  This can be overridden by
prefixing the datatype with the "nullable" flag.  Example::

    "nullable str"


Lists
-----

Lists-types are homogeneous, and are defined as a list of one datatype.

Example::

    ["int"]

Represents a list of ints.  While::

    [{'height': float, 'width': float}]

Represents a list of dictionaries (or "objects").


Tuples
------

Tuples can be heterogeneous, but are fixed width and must have at least two
items.  Again, these are defined as lists of other datatypes::

    ["int", "str"]

Represents a tuple with two items.  The first is an integer, and the second is
a string.


Dictionaries
------------

Dictionaries, or anonymous objects, are defined as dictionaries.  The key of
each item in the dictionary is the property-name, and the value must be
another datatype definition.  Example::

    {'id': 'int', 'name': 'str', 'description': 'str'}

By default, all properties listed on the dictionary are required.  The
following value is invalid, as it lacks the required "description" property::

    {'id': 5, 'name': 'invalid value'}

This behavior can be overridden by prefixing the property-name with the
"optional" flag.  This datatype *is* valid for the value listed above::

    {'id': 'int', 'name': 'str', 'optional description': 'str'}

Arbitrary properties are supported when the wild-card key "_any_" is defined on
the dictionary::

    {'_any_': 'str'}

