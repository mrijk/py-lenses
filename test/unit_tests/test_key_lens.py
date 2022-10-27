from lenses.key_lens import KeyLens, ListKeyLens, ComposedListKeyLens
from lenses.lens import LensError
from lenses.predicate import Predicate


def test_single():
    data = {"x": 42}

    lens = KeyLens[dict, int](key="x")

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


def test_missing_list_key():
    data = {"x": [1, 2, 3]}

    lens_q = ListKeyLens[dict, int](key="q")

    error, result = lens_q(data)

    assert error
    assert isinstance(error, LensError)
    assert error.key == "q"
    assert result is None


def test_missing_composed_list_key():
    data = {"x": []}

    lens_x = ListKeyLens[dict, dict](key="z")
    lens_y = KeyLens[dict, int](key="y")

    lens = lens_x >> lens_y

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert error


def test_missing_composed_list_key_value():
    data = {"x": [{"y": 1}, {}, {"y": 3}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")

    lens = lens_x >> lens_y

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert error


def test_error_in_predicate():
    data = {"x": [1, None, 2]}

    lens_x = ListKeyLens[dict, int](key="x")

    def fail(x: int | None) -> bool:
        if x is not None:
            return x > 1
        else:
            raise ValueError("Disaster")

    fail_if_none = Predicate[int](fail, can_throw=True)

    lens = lens_x >> fail_if_none

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert error

