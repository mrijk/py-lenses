from lenses.key_lens import KeyLens
from lenses.lens import ComposedLens
from lenses.predefined import inc, dec
from lenses.transformer import Transformer
from test.unit_tests.utils import check_against_expected


def test_transformer():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")

    lens = lens_x >> inc

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error
    assert result == 2


def test_two_composed_transformers():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")

    lens = lens_x >> inc >> dec

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error

    assert result == 1


def test_two_combined_transformers():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")

    lens = lens_x >> (inc + dec)

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)
    assert not error

    assert result == (2, 0)


def test_failing_transformer():
    data = {"x": 1}

    lens_x = KeyLens[dict, int](key="x")

    def failure(_: int) -> int:
        raise ValueError("Oh No!")

    fail = Transformer[int, int](failure, can_throw=True)

    lens = lens_x >> fail

    assert isinstance(lens, ComposedLens)

    error, result = lens(data)

    assert error
    assert error.msg == "Transformer has thrown an exception"


def test_transformer_to_json():
    expected = """
    {
        "type": "Transformer",
        "from": "int",
        "to": "int",
        "can_throw": false
    }
    """

    check_against_expected(inc, expected)
