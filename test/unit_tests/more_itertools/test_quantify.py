from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import quantify
from lenses.predefined import gt


def test_quantify():
    data = [True, False, True]

    all = ListLens[bool]()
    do_quantify = quantify()

    lens = all | do_quantify

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 2


def test_quantify_with_predicate():
    data = range(10)

    all = ListLens[int]()
    gt_5 = gt(5)
    do_quantify = quantify(pred=gt_5)

    lens = all | do_quantify

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 4