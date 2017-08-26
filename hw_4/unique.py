import sys


def unique(iterable):
    iterator = iter(iterable)
    try:
        prev = next(iterator)
        yield prev
        while True:
            x = next(iterator)
            if x != prev:
                yield x
            prev = x
    except StopIteration:
        pass

exec(sys.stdin.read())
