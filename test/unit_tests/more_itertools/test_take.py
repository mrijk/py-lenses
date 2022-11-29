from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import take


def test_take():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_two = take(n=2)

    lens = all | take_two

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == [13, 14]
