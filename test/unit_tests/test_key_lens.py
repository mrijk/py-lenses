from lenses.lens import LensError
from lenses.key_lens import KeyLens


def test_single():
    data = {"x": 42}

    lens = KeyLens[dict, str](key="x")

    error, result = lens(data)

    assert not error
    assert result == 42


def test_missing_key():
    data = {"x": 42}

    lens_q = KeyLens[dict, int](key="q")

    error, result = lens_q(data)

    assert error
    assert isinstance(error, LensError)
    assert error.key == "q"
    assert result is None
