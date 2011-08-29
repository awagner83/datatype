
from pytest import raises

from datatype.validation import (BadDatatypeDefinitionError,
        failures, is_valid, _parse_dict_key)


def test_is_valid_primitive():
    assert is_valid("int", 5)


def test_is_valid_object():
    datatype = {"foo": "int"}
    assert is_valid(datatype, {"foo": 5})


def test_failures_primitive():
    assert failures('int', '5') == ['expected int, got str']


def test_failures_unicode_is_str():
    assert failures('str', u'foo') == []


def test_failures_object_missing_property():
    expected = ['missing required property: "foo"']
    assert failures({'foo': 'int'}, {}) == expected


def test_failures_object_wrong_prop_type():
    expected = ['foo: expected int, got str']
    assert failures({'foo': 'int'}, {'foo': 'bar'}) == expected


def test_failures_object_nested():
    datatype = {'foo': {'bar': 'str'}}
    value = {'foo': {'bar': 5}}
    expected = ['foo.bar: expected str, got int']
    assert failures(datatype, value) == expected

    value = {'foo': {}}
    expected = ['foo: missing required property: "bar"']
    assert failures(datatype, value) == expected


def test_failures_object_unexpected_property():
    datatype = {}
    value = {'foo': 'bar'}
    expected = ['unexpected property "foo"']
    assert failures(datatype, value) == expected


def test_failures_object_bad_value():
    datatype = {}
    value = 5
    expected = ['expected dict, got int']
    assert failures(datatype, value) == expected


def test_failures_multiple():
    datatype = {'foo': 'int', 'bar': 'int', 'bif': 'str'}
    value = {'foo': 'a', 'bar': 5, 'bif': 1.0}
    expected = set([
            'foo: expected int, got str',
            'bif: expected str, got float'
        ])
    assert set(failures(datatype, value)) == expected


def test_failures_bad_definition():
    datatype = None
    assert raises(BadDatatypeDefinitionError, failures, datatype, None)


def test_failures_list():
    datatype = ['str']
    assert failures(datatype, ['foo', 'bar', 'baz']) == []


def test_failures_list_failure():
    datatype = ['str']
    assert failures(datatype, ['a', 'b', 3]) == ['[2]: expected str, got int']


def test_failures_optional():
    datatype = {
            'foo': 'int',
            'optional bar': 'int'
        }
    good_value = {'foo': 5}
    bad_value = {'foo': 5, 'bar': 'bif'}

    assert failures(datatype, good_value) == []
    assert failures(datatype, bad_value) == ['bar: expected int, got str']


def test_parse_dict_key():
    assert _parse_dict_key('optional foo') == ('foo', ['optional'])

