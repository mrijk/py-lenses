from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import only


def test_only():
    data = [13]

    all = ListLens[int]()
    select_only = only()

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_only_no_default():
    data = []

    all = ListLens[int]()
    select_only = only()

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result is None


def test_only_with_default():
    data = []

    all = ListLens[int]()
    select_only = only(default=42)

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42
