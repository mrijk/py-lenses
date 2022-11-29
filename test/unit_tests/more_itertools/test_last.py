from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import last


def test_last():
    data = [13, 14]

    all = ListLens[int]()
    select_last = last()

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14


def test_last_no_default():
    data = []

    all = ListLens[int]()
    select_last = last()

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_last_with_default():
    data = []

    all = ListLens[int]()
    select_last = last(default=42)

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42
