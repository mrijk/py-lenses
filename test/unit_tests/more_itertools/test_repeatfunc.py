from operator import add

from lenses.more_itertools import repeatfunc


def test_repeatfunc():
    times = 4
    args = 3, 5
    generator = repeatfunc(add, times, *args)

    error, result = generator()
    assert not error
    assert list(result) == [8, 8, 8, 8]
