datatype - Anonymous datatype validation
========================================

Example:
--------

```python

>>> from datatype.validation import failures

>>> datatype = {'foo': [{'bar': 'int'}]}
>>> bad_value = {'foo': [{'bar': 'baz'}], 'bif': 'pow!'}

>>> failures(datatype, bad_value)
['foo[0].bar: expected int, got str', 'unexpected property "bif"']

```

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

    DEFINITION = PRIMITIVE | LIST | DICTIONARY
    PRIMITIVE = "int" | "str" | "float" | "bool"
    DICTIONARY = {DICTIONARY-KEY: DEFINITION}
    DICTIONARY-KEY = ["optional "] + DICTIONARY-KEY-NAME
    DICTIONARY-KEY-NAME = [A-Za-z0-9_]+
    LIST = [DEFINITION]


Definition Examples (in python):
--------------------------------

    definition: "int"
    example value: 5

    definition: {"foo": "int"}
    example value: {"foo": 5}

    definition: [{"foo": ["bool"]}]
    example value: [{"foo": [True, False]}, {"foo": [False, False]}]


Copyright and License
---------------------

Copyright 2011 LearningStation, Inc.

Licensed under the BSD-3 License.  You may obtain a copy of the License in the
LICENSE file.

