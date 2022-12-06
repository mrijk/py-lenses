from lenses.key_lens import KeyLens, ListKeyLens, ComposedListKeyLens, DictLens
from lenses.lens import LensError
from lenses.predicate import Predicate
from test.unit_tests.utils import check_against_expected


def test_single():
    data = {"x": 42}

    lens = DictLens[int](key="x")

    error, result = data >> lens

    assert not error
    assert result == 42


def test_missing_key():
    data = {"x": 42}

    lens_q = DictLens[int](key="q")

    error, result = lens_q(data)

    assert error
    assert isinstance(error, LensError)
    assert error.key == "q"
    assert result is None


def test_missing_list_key():
    data = {"x": [1, 2, 3]}

    lens_q = DictLens[int](key="q")

    error, result = lens_q(data)

    assert error
    assert isinstance(error, LensError)
    assert error.key == "q"
    assert result is None


def test_missing_composed_list_key():
    data = {"x": []}

    lens_x = ListKeyLens[dict, dict](key="z")
    lens_y = DictLens[int](key="y")

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


def test_list_key_lens():
    data = {"x": {"y": [1, 2, 3]}}

    lens_x = DictLens[dict](key="x")
    lens_y = ListKeyLens[dict, int](key="y")

    lens = lens_x >> lens_y

    # assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [1, 2, 3]


def test_key_lens_to_json():
    lens = DictLens[int](key="x")

    expected = """
    {
        "type": "KeyLens", 
        "from": "dict", 
        "to": "int", 
        "key": "x"
    }
    """

    check_against_expected(lens, expected)
