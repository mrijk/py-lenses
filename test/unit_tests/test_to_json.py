import json

from lenses.key_lens import DictLens
from lenses.lens import ListLens
from lenses.predicate import Predicate


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


def test_composed_2_lens_to_json():
    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x | lens_y

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


def test_combined_2_lens_to_json():
    lens_x = DictLens[int](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x + lens_y

    expected = """
    {
        "type": "Combined2Lens",
        "from": "dict",
        "to": "tuple[int, int]",
        "lenses": [
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "int",
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


def test_combined_3_lens_to_json():
    lens_x = DictLens[int](key="x")
    lens_y = DictLens[float](key="y")
    lens_z = DictLens[str](key="z")

    lens = lens_x + lens_y + lens_z

    expected = """
    {
        "type": "Combined3Lens",
        "from": "dict",
        "to": "tuple[int, float, str]",
        "lenses": [
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "int",
                "key": "x"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "float",
                "key": "y"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "str",
                "key": "z"
            }
        ]
    }
    """

    check_against_expected(lens, expected)


def test_combined_4_lens_to_json():
    lens_x = DictLens[int](key="x")
    lens_y = DictLens[float](key="y")
    lens_z = DictLens[str](key="z")
    lens_w = DictLens[dict](key="w")

    lens = lens_x + lens_y + lens_z + lens_w

    expected = """
    {
        "type": "Combined4Lens",
        "from": "dict",
        "to": "tuple[int, float, str, dict]",
        "lenses": [
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "int",
                "key": "x"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "float",
                "key": "y"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "str",
                "key": "z"
            },
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "dict",
                "key": "w"
            }
        ]
    }
    """

    check_against_expected(lens, expected)


def test_composed_and_combined_to_json():
    lens_x = DictLens[dict](key="x")
    lens_y = DictLens[str](key="y")
    lens_z = DictLens[str](key="z")

    lens = lens_x | (lens_y + lens_z)

    expected = """
    {
        "type": "ComposedLens",
        "from": "dict",
        "to": "tuple[str, str]",
        "lenses": [
            {
                "type": "KeyLens",
                "from": "dict",
                "to": "dict",
                "key": "x"
            },
            {
                "type": "Combined2Lens",
                "from": "dict",
                "to": "tuple[str, str]",
                "lenses": [
                    {
                        "type": "KeyLens",
                        "from": "dict",
                        "to": "str",
                        "key": "y"
                    },
                    {
                        "type": "KeyLens",
                        "from": "dict",
                        "to": "str",
                        "key": "z"
                    }
                ]
            }
        ]
    }
    """

    check_against_expected(lens, expected)


def test_list_lens_to_json():
    lens = ListLens[dict]()

    expected = """
    {
        "type": "ListLens",
        "from": "list[dict]",
        "to": "list[dict]"
    }
    """

    check_against_expected(lens, expected)


def test_predicate_to_json():
    gt_13 = Predicate[int](lambda x: x > 13)

    expected = """
    {
        "type": "Predicate",
        "from": "int",
        "to": "bool"
    }
    """

    check_against_expected(gt_13, expected)


def check_against_expected(lens, expected):
    result = lens.to_json()
    assert json.loads(json.dumps(result)) == json.loads(expected)