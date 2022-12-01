from lenses.more_itertools import tabulate, take


def test_tabulate():
    source = tabulate(lambda x: x ** 2, start=-3)
    take_4 = take(4)

    generator = source | take_4

    error, result = generator()
    assert not error
    assert list(result) == [9, 4, 1, 0]