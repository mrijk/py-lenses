from lenses.dict_item_lens import DictItemLens, key, value, to_dict
from lenses.transformer import Transformer
from test.unit_tests.utils import check_against_expected


def test_basic():
    data = {"x": 1, "y": 2, "z": 3}

    lens = DictItemLens()

    error, result = lens(data)

    assert not error
    assert result == [("x", 1), ("y", 2), ("z", 3)]


def test_keys():
    data = {"x": 1, "y": 2, "z": 3}

    lens_dict = DictItemLens()

    lens = lens_dict >> key

    error, result = lens(data)

    assert not error
    assert result == ("x", "y", "z")


def test_values():
    data = {"x": 1, "y": 2, "z": 3}

    lens_dict = DictItemLens()

    lens = lens_dict >> value

    result = lens(data)

    assert result.value() == (1, 2, 3)


def test_serde():
    """Serialize and back to dict"""
    data = {"x": 1, "y": 2, "z": 3}

    lens_dict = DictItemLens()

    lens = lens_dict >> (key + value) | to_dict

    error, result = lens(data)

    assert not error
    assert result == data


def test_to_json():
    lens = DictItemLens()

    expected = """
    {
        "type": "DictItemLens"
    }
    """

    check_against_expected(lens, expected)
