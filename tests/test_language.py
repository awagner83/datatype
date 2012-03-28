"""Tests for language module."""

from datatype.language import typename, choice, named, reference, literal


def test_typename():
    assert typename('int') == 'type'
    assert typename({'_type_': 'choice'}) == 'choice'
    assert typename({'_type_': 'foo'}) == 'foo'
    assert typename({}) == 'type'
    assert typename([]) == 'type'


def test_choice():
    assert choice('str', 'int') == {
            '_type_': 'choice', 'choices': ['str', 'int']}


def test_named():
    assert named('foo', 'str') == {
            '_type_': 'named', 'name': 'foo', 'value': 'str'}


def test_reference():
    assert reference('foo') == {'_type_': 'reference', 'name': 'foo'}


def test_literal():
    assert literal('str') == {'_type_': 'literal', 'value': 'str'}

