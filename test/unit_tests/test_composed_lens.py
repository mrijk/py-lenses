from lenses.key_lens import DictLens
from lenses.lens import ComposedLens
from test.unit_tests.utils import check_against_expected


def test_two_lenses():
    data = {"x": {"y": 42}}

    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    error, result = data >> lens_x >> lens_y

    assert not error
    assert result == 42


def test_two_lenses_call():
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


def test_three_lenses_call():
    data = {"x": {"y": {"z": 42}}}

    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[dict](key="y")
    lens_z = DictLens[int](key="z")

    lens = lens_x >> lens_y >> lens_z

    assert isinstance(lens, ComposedLens)

    error, result = data >> lens_x >> lens_y >> lens_z

    assert not error
    assert result == 42


def test_composed_2_lens_to_json():
    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x >> lens_y

    expected = """
    {
        "type": "ComposedLens",
        "from": "dict",
        "to": "int",
        "lenses": [
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "dict",
                "key": "x"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "int",
                "key": "y"
            }
        ]
    }
    """

    check_against_expected(lens, expected)