from lenses.key_lens import DictLens, ListKeyLens, NullableDictLens
from lenses.predefined import not_none


def test_nullable_lens():
    data = {}

    lens = NullableDictLens[int](key="x")

    error, result = lens(data)

    assert not error
    assert result is None


def test_nested_2_nullable_lens():
    data = {}

    lens_x = NullableDictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x >> lens_y

    error, result = lens(data)

    assert not error
    assert result is None


def test_nested_3_nullable_lens():
    data = {}

    lens_x = NullableDictLens[dict](key="x")
    lens_y = DictLens[dict](key="y")
    lens_z = DictLens[str](key="z")

    lens = lens_x >> lens_y >> lens_z

    error, result = lens(data)

    assert not error
    assert result is None


def test_combined_nullable_lens():
    data = {
        "x": [{"y": 1}, {"z": 2}]
    }

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = NullableDictLens[int](key="y")

    lens = lens_x >> lens_y

    error, result = lens(data)

    assert not error
    assert result == [1, None]
