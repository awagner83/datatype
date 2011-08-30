
from datatype.docgen import add_docs, gendocs, getindent


def test_gendocs():
    assert gendocs('int') == "Return datatype:\n    'int'"


def test_getindent():
    assert getindent("""Foo

            bar
            baz""") == 12


def test_add_docs():
    def foo():
        """some

        multiline
        docstring."""
        pass

    add_docs(foo, 'int')

    expected = ("""some

        multiline
        docstring.

        Return datatype:
            'int'""")

    print foo.__doc__
    print expected

    assert foo.__doc__ == expected

