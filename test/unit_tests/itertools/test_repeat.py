from lenses.itertools import repeat
from lenses.more_itertools import take


def test_repeat():
    infinite = repeat(10)
    take_4 = take(4)

    generator = infinite | take_4

    error, result = generator()

    assert not error
    assert result == [10, 10, 10, 10]


def test_repeat_with_times():
    infinite = repeat(10, times=3)

    generator = infinite

    error, result = generator()

    assert not error
    assert list(result) == [10, 10, 10]