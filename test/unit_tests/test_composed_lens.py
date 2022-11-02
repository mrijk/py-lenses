from lenses.key_lens import KeyLens, DictLens
from lenses.lens import ComposedLens


def test_two_lenses():
    data = {"x": {"y": 42}}

    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x >> lens_y

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)

    assert not error
    assert result == 42


def test_three_lenses():
    data = {"x": {"y": {"z": 42}}}

    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[dict](key="y")
    lens_z = DictLens[int](key="z")

    lens = lens_x >> lens_y >> lens_z

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)

    assert not error
    assert result == 42
