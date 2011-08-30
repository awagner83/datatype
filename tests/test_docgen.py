
from datatype.docgen import gendocs


def test_gendocs():
    assert gendocs('int') == "Return datatype:\n    'int'"

