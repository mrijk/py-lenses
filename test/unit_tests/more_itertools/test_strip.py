from typing import Any

from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import strip
from lenses.predefined import to_list


def test_strip():
    data = [None, False, None, 1, 2, None, 3, False, None]

    all = ListLens[Any]()
    strip_falsy = strip(pred=lambda x: x in {None, False, ''})

    lens = all | strip_falsy | to_list

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == [1, 2, None, 3]
