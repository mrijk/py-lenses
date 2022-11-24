from lenses.inject_lens import InjectLens
from lenses.key_lens import KeyLens
from lenses.transformer import Transformer
from test.unit_tests.utils import check_against_expected


def test_inject():
    inject_5 = InjectLens(y=5, z=42)

    error, result = inject_5(13)

    assert not error
    assert result == (13, {"y": 5, "z": 42})


def test_composed_inject():
    def add(x: int, y: int):
        return x + y

    data = {"x": 42}

    lens_x = KeyLens[dict, int](key="x")
    inject_5 = InjectLens(y=5)
    add = Transformer[int, int](add)

    lens = lens_x | inject_5 | add

    error, result = lens(data)

    assert not error
    assert result == 47


def test_to_json():
    inject_5 = InjectLens(y=5)

    expected = """
    {
        "type": "InjectLens",
        "args": {
            "y": 5
        }
    }
    """

    check_against_expected(inject_5, expected)
