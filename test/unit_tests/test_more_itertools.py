from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import one


def test_one_happy():
    data = [13]

    all = ListLens[int]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_one_to_short():
    data = []

    all = ListLens[dict]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_one_to_long():
    data = [13, 14]

    all = ListLens[int]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error
