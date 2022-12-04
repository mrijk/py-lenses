from lenses.itertools import cycle
from lenses.more_itertools import take


def test_cycle():
    infinite = cycle[str]("ABC")
    take_6 = take(6)

    generator = infinite | take_6

    error, result = generator()

    assert not error
    assert result == ['A', 'B', 'C', 'A', 'B', 'C']