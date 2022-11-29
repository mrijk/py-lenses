from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import nth_or_last


def test_nth_or_last_return_last():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_last = nth_or_last(n=13)

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 15


