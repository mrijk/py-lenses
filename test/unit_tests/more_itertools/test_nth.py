from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import nth, nth_or_last


def test_nth():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth(n=1)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14


def test_nth_with_default():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth(n=13, default=666)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 666


def test_nth_or_last():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth_or_last(n=1)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14
