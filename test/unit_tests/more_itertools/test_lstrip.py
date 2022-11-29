from typing import Any

from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import lstrip


def test_lstrip():
    data = [None, False, None, 1, 2, None, 3, False, None]

    all = ListLens[Any]()
    strip_falsy = lstrip(pred=lambda x: x in {None, False, ''})

    # TODO
    lens = all | strip_falsy # | to_list

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == [1, 2, None, 3, False, None]
