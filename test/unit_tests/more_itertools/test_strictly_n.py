from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import strictly_n


def test_strictly_n():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_three = strictly_n(3)

    lens = all | take_three

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == [13, 14, 15]


def test_strictly_n_too_short():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_four = strictly_n(4)

    lens = all | take_four

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_strictly_n_too_long():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_two = strictly_n(4)

    lens = all | take_two

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_strictly_n_too_short_intercepted():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_four = strictly_n(4, too_short=lambda item_count: item_count)

    lens = all | take_four

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == data


def test_strictly_n_too_long_intercepted():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_two = strictly_n(2, too_long=lambda item_count: item_count)

    lens = all | take_two

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == [13, 14]
