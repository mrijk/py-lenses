from lenses.key_lens import KeyLens
from lenses.transformer import Transformer


def test_transformer():
    data = {"x": 1}

    def inc(x: int) -> int:
        return x + 1

    lens_x = KeyLens[dict, int](key="x")
    transform = Transformer[int, int](inc)

    lens = lens_x | transform

    error, result = lens(data)
    assert not error
    assert result == 2
