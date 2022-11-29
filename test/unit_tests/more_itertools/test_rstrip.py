from typing import Any

from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import rstrip


def test_rstrip():
    data = [None, False, None, 1, 2, None, 3, False, None]

    all = ListLens[Any]()
    strip_falsy = rstrip(pred=lambda x: x in {None, False, ''})

    # TODO
    lens = all | strip_falsy # | to_list

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == [None, False, None, 1, 2, None, 3]
