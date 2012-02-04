from pytest import raises

from datatype.decorators import BadReturnValueError, returns, returns_iter


def test_returns():
    @returns({'foo': 'int'})
    def good_function():
        return {'foo': 5}

    # datatype should be 'transparent' when all is well
    assert good_function() == {'foo': 5}


def test_returns_failure():
    @returns('bool')
    def bad_function():
        return 5

    ex = raises(BadReturnValueError, bad_function)
    assert ex
    assert ex.value.failures == ['expected bool, got int']


def test_returns_strict():
    val = {'expected': True, 'spanish inquisition': False}

    @returns({'expected': 'bool'})
    def too_much_stuff():
        return val

    ex = raises(BadReturnValueError, too_much_stuff)
    assert ex
    assert 'unexpected property' in ex.value.failures[0]

    @returns({'expected': 'bool'}, strict=False)
    def still_too_much_stuff():
        return val

    assert still_too_much_stuff()


def test_returns_function_meta():
    @returns('int')
    def my_function():
        """My Docs"""
        return 5

    assert my_function.__name__ == 'my_function'
    assert my_function.__doc__ == "My Docs\n\nReturn datatype:\n    'int'"


def test_returns_iter():
    @returns_iter('int')
    def good_function():
        yield 5
        yield 6

    # datatype should be transparent (and not consume things too early)
    iter_result = good_function()
    assert list(iter_result) == [5, 6]


def test_returns_iter_fail():
    @returns_iter('int')
    def bad_function():
        yield 5
        yield 'foo'

    # exception won't be raised immediately
    iter_result = bad_function()
    ex = raises(BadReturnValueError, list, iter_result)
    assert ex.value.failures == ['expected int, got str']


def test_returns_iter_strict():
    val = {'expected': True, 'spanish inquisition': False}

    @returns_iter({'expected': 'bool'})
    def too_much_stuff():
        yield val

    iter_result = too_much_stuff()
    ex = raises(BadReturnValueError, list, iter_result)
    assert ex
    assert 'unexpected property' in ex.value.failures[0]

    @returns_iter({'expected': 'bool'}, strict=False)
    def still_too_much_stuff():
        yield val

    assert list(still_too_much_stuff())

