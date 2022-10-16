from lenses.inject_lens import InjectLens
from lenses.key_lens import KeyLens
from lenses.transformer import Transformer


def test_inject():
    def add(x: int, y: int):
        return None, x + y

    data = {"x": 42}

    lens_x = KeyLens[dict, int](key="x")
    inc = Transformer[int, int](add)

    lens = lens_x | InjectLens(y=5) | inc

    error, result = lens(data)

    assert not error
    assert result == (None, 47)
