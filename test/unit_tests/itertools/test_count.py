from lenses.itertools import count
from lenses.more_itertools import take


def test_count():
    infinite = count()
    take_4 = take(4)

    generator = infinite | take_4

    error, result = generator()

    assert not error
    assert result == [0, 1, 2, 3]


def test_count_with_start():
    from_10 = count(start=10)
    take_4 = take(4)

    generator = from_10 | take_4

    error, result = generator()

    assert not error
    assert result == [10, 11, 12, 13]


def test_count_with_step():
    from_2_5 = count(start=2.5, step=0.5)
    take_4 = take(4)

    generator = from_2_5 | take_4

    error, result = generator()

    assert not error
    assert result == [2.5, 3.0, 3.5, 4.0]
