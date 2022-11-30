from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import first_true
from lenses.predefined import gt


def test_first_true():
    data = range(10)

    all = ListLens[int]()
    select_first_true = first_true()

    lens = all | select_first_true

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 1


def test_first_true_with_default():
    data = [False, False]

    all = ListLens[bool]()
    select_first_true = first_true(default="missing")

    lens = all | select_first_true

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == "missing"


def test_first_true_with_predicate():
    data = range(10)

    all = ListLens[int]()
    gt_5 = gt(5)
    select_first_true = first_true(default="missing", pred=gt_5)

    lens = all | select_first_true

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 6
