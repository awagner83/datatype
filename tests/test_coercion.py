from datatype.coercion import coerce_value


def test_coerce_value():
    assert coerce_value('int', '5') == 5
    assert coerce_value(['str'], [1, 2, 3]) == ['1', '2', '3']
    assert coerce_value({'foo': 'float'}, {'foo': 2}) == {'foo': 2.0}


def test_coerce_failure():
    assert coerce_value('int', 'foo') == 'foo'
    assert coerce_value(['int'], ['1', 2, 'foo']) == [1, 2, 'foo']

