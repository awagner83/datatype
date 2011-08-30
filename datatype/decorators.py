from functools import wraps

from datatype.validation import failures
from datatype.docgen import add_docs


class BadReturnValueError(Exception):
    """Raised when `returns` decorator encounters a return value
    not matching it's given datatype."""

    # List of things that went wrong in validation
    failures = []


def returns(dfn):
    """Make decorators to watch return values of functions to ensure
    they match the given datatype definition.

    Example:
        >>> @returns('int')
        ... def myfunction():
        ...     return "bad return value"
        >>> myfunction()
        Traceback (most recent call last):
        BadReturnValueError
    """
    def decorator(fn):

        # Add return-datatype info to function doc-block
        add_docs(fn, dfn)

        @wraps(fn)
        def wrapped_function(*args, **kwargs):
            ret = fn(*args, **kwargs)

            # Check for failure and raise
            fails = failures(dfn, ret)
            if fails:
                ex = BadReturnValueError()
                ex.failures = fails
                raise ex

            # All is well, return as usual
            return ret
        return wrapped_function
    return decorator

