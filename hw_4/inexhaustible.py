import sys
from functools import wraps


def inexhaustible(generator):
    @wraps(generator)
    def decorated(*args, **kwargs):
        class new_generator():
            def __init__(self):
                pass

            def __next__(self):
                return next(self.x)

            def __iter__(self):
                self.x = generator(*args, **kwargs)
                return iter(self.x)

        return new_generator()
    return decorated

exec(sys.stdin.read())
