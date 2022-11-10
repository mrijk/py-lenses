from typing import Any

from lenses.key_lens import DictLens, ListKeyLens, NullableDictLens
from lenses.predefined import not_none
from lenses.predicate import Predicate


def test_nullable_lens():
    data = {}

    lens = NullableDictLens[int | None](key="x")

    error, result = lens(data)

    assert not error
    assert result is None


def test_nested_nullable_lens():
    data = {}

    lens_x = NullableDictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x >> lens_y

    error, result = lens(data)

    assert not error
    assert result is None


def test_combined_nullable_lens():
    data = {
        "x": [{"y": 1}, {"z": 2}]
    }

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = NullableDictLens[int](key="y")

    lens = lens_x >> lens_y >> not_none

    error, result = lens(data)

    assert not error
    assert result == [1]
