from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import first


def test_first():
    data = [13, 14]

    all = ListLens[int]()
    select_first = first()

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_first_no_default():
    data = []

    all = ListLens[int]()
    select_first = first()

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_first_with_default():
    data = []

    all = ListLens[int]()
    select_first = first(default=42)

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42
