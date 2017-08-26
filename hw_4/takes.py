import sys
from functools import wraps


def takes(*argstypes):
    def check_return_types(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            for i, arg in enumerate(args):
                if i > len(argstypes) - 1:
                    break
                if not isinstance(arg, argstypes[i]):
                    raise TypeError
            return func(*args, **kwargs)
        return decorated
    return check_return_types

exec(sys.stdin.read())
