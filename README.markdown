datatype - Anonymous datatype validation
========================================

Datatype definitions
--------------------

Datatype definitions are represented with a small set of types that should be
built-in for *most* languages.

Required types for proper validation:
 - int
 - float
 - string
 - boolean
 - dictionary (or anonymous object)
 - list (or array)

Specification
-------------

    DEFINITION = PRIMITIVE|LIST|DICTIONARY
    PRIMITIVE = "int" | "str" | "float" | "bool"
    DICTIONARY = {DICTIONARY-KEY: PRIMITIVE|DICTIONARY|LIST}
    DICTIONARY-KEY = ["optional "] + DICTIONARY-KEY-NAME
    DICTIONARY-KEY-NAME = [A-Za-z0-9_]+
    LIST = [PRIMITIVE|DICTIONARY|LIST]

Definition Examples (in python):
--------------------------------

    definition: "int"
    example value: 5

    definition: {"foo": "int"}
    example value: {"foo": 5}

    definition: [{"foo": ["bool"]}]
    example value: [{"foo": [True, False]}, {"foo": [False, False]}]

