import sys


class AssertRaises(object):
    def __init__(self, exc_type):
        self.exception_type = exc_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            raise AssertionError
        exc = exc_type()
        if isinstance(exc, self.exception_type):
            return self.exception_type
        else:
            raise AssertionError

exec(sys.stdin.read())
