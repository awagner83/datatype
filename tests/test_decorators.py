from pytest import raises

from datatype.decorators import BadReturnValueError, returns


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
