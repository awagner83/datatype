datatype - Anonymous datatype validation
========================================

Examples
--------
::

    >>> from datatype.validation import failures

    >>> datatype = {'foo': [{'bar': 'int'}]}
    >>> bad_value = {'foo': [{'bar': 'baz'}], 'bif': 'pow!'}

    >>> failures(datatype, bad_value)
    ['foo[0].bar: expected int, got str', 'unexpected property "bif"']


Wildcard dictionary keys::

    >>> datatype = {'_any_': ['int']}
    >>> good_value = {'foo': [1, 2, 3], 'bar': [3, 4, 5]}

    >>> failures(datatype, good_value)
    []


Datatype Definitions
--------------------

Datatype definitions are represented with a small set of types that should be
built-in for *most* languages.

Required types for proper validation:

* int
* float
* string
* boolean
* dictionary (or anonymous object)
* list (or array)


Specification
-------------
::

    DEFINITION = PRIMITIVE | LIST | DICTIONARY | TUPLE
    PRIMITIVE = ["nullable "] + ("int" | "str" | "float" | "bool")
    DICTIONARY = (dictionary of) key: DICTIONARY-KEY, value: DEFINITION
    DICTIONARY-KEY = (["optional "] + DICTIONARY-KEY-NAME) | "_any_"
    DICTIONARY-KEY-NAME = [A-Za-z0-9_]+
    LIST = (list of one) DEFINITION
    TUPLE = (list of more than one) DEFINITION


Definition Examples (in python)
-------------------------------
::

    definition: "int"
    example value: 5

    definition: {"foo": "int"}
    example value: {"foo": 5}

    definition: [{"foo": ["bool"]}]
    example value: [{"foo": [True, False]}, {"foo": [False, False]}]

    definition: {"_any_": "int"}
    example value: {"foo": 5, "bar": 7}

    definition: ["int", "str"]
    example value: [5, "foo"]


Copyright and License
---------------------

Copyright 2011 LearningStation, Inc.

Licensed under the BSD-3 License.  You may obtain a copy of the License in the
LICENSE file.

