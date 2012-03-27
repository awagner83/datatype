"""Tests for datatype internal utility functions."""

from mock import Mock, call

from datatype.tools import (Choice, datatype_type, extract_named_types, walk)


# walk_test_data :: [(datatype, value, callback_call_args_list)]
walk_test_data = [
        (   # primitive
            'int', 5,
            [call('', 'int', 5, [])]
        ),
        (   # nullable primitive
            'nullable str', None,
            [call('', 'str', None, ['nullable'])]
        ),
        (   # list
            ['str'], ['a', 'b', 'c'],
            [
                call('', ['str'], ['a', 'b', 'c'], []),
                call('[0]', 'str', 'a', []),
                call('[1]', 'str', 'b', []),
                call('[2]', 'str', 'c', []),
            ]
        ),
        (   # tuple
            ['int', 'str'], [5, 'foo'],
            [
                call('', ['int', 'str'], [5, 'foo'], []),
                call('[0]', 'int', 5, []),
                call('[1]', 'str', 'foo', []),
            ]
        ),
        (   # dictionary
            {'foo': 'int'}, {'foo': 5},
            [
                call('', {'foo': 'int'}, {'foo': 5}, []),
                call('foo', 'int', 5, []),
            ]
        ),
        (   # dictionary (with optional key, and value without key)
            {'optional bar': 'str'}, {},
            [
                call('', {'optional bar': 'str'}, {}, []),
            ]
        ),
        (   # dictionary (with optional key, and value with key)
            {'optional bar': 'str'}, {'bar': 'baz'},
            [
                call('', {'optional bar': 'str'}, {'bar': 'baz'}, []),
                call('bar', 'str', 'baz', []),
            ]
        ),
        (   # choice datatype
            {'_type_': 'choice', 'choices': ['int', 'str']}, 'foo',
            [
                call('', Choice(['int', 'str']), 'foo', []),
            ]
        ),
    ]


extract_named_types_data = [
        (   # unnamed primitive
            'str', {}, 'str'
        ),
        (   # named primitive
            {'_type_': 'named', 'name': 'foo', 'value': 'str'},
            {'foo': 'str'}, 'str'
        ),
        (   # named in list
            [{'_type_': 'named', 'name': 'bar', 'value': 'int'}],
            {'bar': 'int'}, ['int']
        ),
        (   # named nested in named
            {'_type_': 'named', 'name': 'foo', 'value': {
                'bar': {'_type_': 'named', 'name': 'baz', 'value': 'bool'}}},
            {'foo': {'bar': 'bool'}, 'baz': 'bool'}, {'bar': 'bool'}
        )
    ]


def pytest_generate_tests(metafunc):
    if "walk_test" in metafunc.funcargnames:
        metafunc.parametrize("walk_test", walk_test_data)
    if "extract_types_test" in metafunc.funcargnames:
        metafunc.parametrize("extract_types_test", extract_named_types_data)


def test_walk(walk_test):
    datatype, actual, call_args_list = walk_test
    callback_mock = Mock()

    result = walk(datatype, actual, callback_mock)
    assert callback_mock.call_args_list == call_args_list
    assert result == actual


def test_extract_named_types(extract_types_test):
    datatype, named_dict, refined_type = extract_types_test

    actual_named_dict, actual_refined = extract_named_types(datatype)
    assert actual_named_dict == named_dict
    assert actual_refined == refined_type


def test_choice_obj():
    assert str(Choice(['str', 'int'])) == 'str or int'
    assert str(Choice(['str', 'int', 'bool'])) == 'str, int, or bool'
    assert repr(Choice([1])) == "<Choice of [1]>"
    assert list(Choice([1, 2, 3])) == [1, 2, 3]
    assert Choice([1]) == Choice([1])
    assert Choice([1]) != Choice([2])


def test_datatype_type():
    assert datatype_type('int') == 'type'
    assert datatype_type({'_type_': 'choice'}) == 'choice'
    assert datatype_type({'_type_': 'foo'}) == 'foo'
    assert datatype_type({}) == 'type'
    assert datatype_type([]) == 'type'

