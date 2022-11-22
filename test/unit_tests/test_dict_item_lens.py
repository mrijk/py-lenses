from lenses.dict_item_lens import DictItemLens
from test.unit_tests.utils import check_against_expected


def test_basic():
    data = {"x": 1, "y": 2, "z": 3}

    lens = DictItemLens()

    error, result = lens(data)

    assert not error
    assert result == [("x", 1), ("y", 2), ("z", 3)]


def test_to_json():
    lens = DictItemLens()

    expected = """
    {
        "type": "DictItemLens"
    }
    """

    check_against_expected(lens, expected)
