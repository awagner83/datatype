from collections import defaultdict

from pytest import raises

from datatype.tools import Choice
from datatype.validation import (failures, is_valid, validate_step)


def test_is_valid_primitive():
    assert is_valid("int", 5)
    assert not is_valid("int", True)


def test_is_valid_object():
    datatype = {"foo": "int"}
    assert is_valid(datatype, {"foo": 5})


def test_is_valid_object_funny_name():
    datatype = {'no': 'int'}
    assert is_valid(datatype, {'no': 3})


def test_failures_primitive():
    assert failures('int', '5') == ['expected int, got str']


def test_failures_unicode_is_str():
    assert failures('str', u'foo') == []


def test_failures_nullable():
    assert failures('nullable int', None) == []
    assert failures('int', None) == ['unexpected null for non-nullable type']


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


def test_failures_object_arbitrary_key():
    datatype = {'_any_': 'int'}
    good_value = {'foo': 5, 'bar': 6, 'baz': 7}
    bad_balue = {'foo': 'five'}
    assert failures(datatype, good_value) == []
    assert failures(datatype, bad_balue) == ['foo: expected int, got str']


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


def test_failures_object_defaultdict():
    datatype = {}
    value = defaultdict(int)
    expected = []
    assert failures(datatype, value) == expected


def test_failures_multiple():
    datatype = {'foo': 'int', 'bar': 'int', 'bif': 'str'}
    value = {'foo': 'a', 'bar': 5, 'bif': 1.0}
    expected = set([
            'foo: expected int, got str',
            'bif: expected str, got float'
        ])
    assert set(failures(datatype, value)) == expected


def test_failures_list():
    datatype = ['str']
    assert failures(datatype, ['foo', 'bar', 'baz']) == []


def test_failures_list_failure():
    datatype = ['str']
    assert failures(datatype, ['a', 'b', 3]) == ['[2]: expected str, got int']


def test_failures_tuple():
    datatype = ['str', 'int']
    assert failures(datatype, ['foo', 5]) == []


def test_failures_tuple_failure():
    datatype = ['str', 'int']
    assert failures(datatype, ['foo']) == ['missing required value at index 1']
    assert failures(datatype, ['foo', 5, True]
            ) == ['unexpected value at index 2']


def test_failures_optional():
    datatype = {
            'foo': 'int',
            'optional bar': 'int'
        }
    good_value = {'foo': 5}
    bad_value = {'foo': 5, 'bar': 'bif'}

    assert failures(datatype, good_value) == []
    assert failures(datatype, bad_value) == ['bar: expected int, got str']


def test_failures_choice():
    datatype = {
            '_type_': 'choice',
            'choices': ['int', 'str']
        }

    assert failures(datatype, 5) == []
    assert failures(datatype, 'foo') == []
    assert failures(datatype, {}) == ['{} is none of expected int or str']


def test_failures_recursive():
    datatype = {
            '_type_': 'named',
            'name': 'person',
            'value': {
                'name': 'str',
                'children': [{'_type_': 'reference', 'name': 'person'}]
            }
        }

    good_value = {
            'name': 'bob',
            'children': [
                {
                    'name': 'frank',
                    'children': []
                },
                {
                    'name': 'jane',
                    'children': [
                        {'name': 'alfred', 'children': []}
                    ]
                }
            ]
        }
    assert failures(datatype, good_value) == []

    bad_value = {}
    assert failures(datatype, bad_value) == [
            'missing required property: "name"',
            'missing required property: "children"']

    bad_value2 = {
            'name': 'fred',
            'children': [{'name': 'jim'}]
        }
    assert failures(datatype, bad_value2) == [
            'children[0]: missing required property: "children"'
        ]


def test_failures_literal():
    datatype = {'_type_': 'literal', 'value': 'foo'}
    assert failures(datatype, 'bar') == [
        'expected literal value "foo", got "bar"']

