datatype - Anonymous datatype validation and coercion
=====================================================

For full package documenation, please see: http://datatype.readthedocs.org/

Examples
--------
::

    >>> from datatype.validation import failures

    >>> datatype = {'foo': [{'bar': 'int'}]}
    >>> bad_value = {'foo': [{'bar': 'baz'}], 'bif': 'pow!'}

    >>> failures(datatype, bad_value)
    ['unexpected property "bif"', 'foo[0].bar: expected int, got str']


Wildcard dictionary keys::

    >>> datatype = {'_any_': ['int']}
    >>> good_value = {'foo': [1, 2, 3], 'bar': [3, 4, 5]}

    >>> failures(datatype, good_value)
    []


Coercion::

    >>> from datatype.coercion import coerce_value

    >>> coerce_value(['str'], [1, 2, 3])
    ['1', '2', '3']


Copyright and License
---------------------

Copyright 2011-2012 LearningStation, Inc. and Adam Wagner

Licensed under the BSD-3 License.  You may obtain a copy of the License in the
LICENSE file.

