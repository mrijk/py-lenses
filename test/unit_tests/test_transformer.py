from lenses.key_lens import KeyLens
from lenses.lens import ComposedLens
from lenses.transformer import Transformer


def test_transformer():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")
    inc = Transformer[int, int](lambda x: x + 1)

    lens = lens_x >> inc

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error
    assert result == 2


def test_two_composed_transformers():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")
    inc = Transformer[int, int](lambda x: x + 1)
    dec = Transformer[int, int](lambda x: x - 1)

    lens = lens_x >> inc >> dec

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error

    assert result == 1


def test_two_combined_transformers():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")
    inc = Transformer[int, int](lambda x: x + 1)
    dec = Transformer[int, int](lambda x: x - 1)

    lens = lens_x >> (inc + dec)

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error

    assert result == (2, 0)
