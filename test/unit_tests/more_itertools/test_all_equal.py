import pytest as pytest

from lenses.lens import ListLens
from lenses.more_itertools import all_equal


@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 1, 1], True),
        ("aaa", True),
        ([1, 1, 2], False),
        ("aab", False),
    ]
)
def test_all_equal(data, expected):
    all = ListLens[int]()

    lens = all | all_equal

    error, result = lens(data)

    assert not error
    assert result is expected


