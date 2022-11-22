import json


from lenses.key_lens import DictLens, NullableDictLens, ListKeyLens
from lenses.lens import ListLens
from lenses.predefined import inc, count
from lenses.predicate import Predicate
from test.unit_tests.utils import check_against_expected


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


def test_nullable_key_lens_to_json():
    lens = NullableDictLens[int](key="x")

    expected = """
    {
        "type": "NullableKeyLens", 
        "from": "dict", 
        "to": "int | None", 
        "key": "x"
    }
    """

    check_against_expected(lens, expected)


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


def test_nullable_composed_lens_to_json():
    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = NullableDictLens[int](key="y")

    lens = lens_x >> lens_y

    expected = """
    {
        "type": "ComposedListKeyLens",
        "from": "dict",
        "to": "int | None",
        "lens": {
            "type": "NullableKeyLens", 
            "from": "dict", 
            "to": "int | None", 
            "key": "y"
        }
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


def test_list_key_lens_to_json():
    lens = ListKeyLens[dict, bool](key="x")

    expected = """
    {
        "type": "ListKeyLens",
        "from": "list[dict]",
        "to": "list[bool]",
        "key": "x"
    }
    """

    check_against_expected(lens, expected)


def test_flatten_list_lens_to_json():
    lens_all = ListLens[dict]()

    lens = lens_all | count

    expected = """
    {
        "type": "FlattenListLens",
        "from": "list[dict]",
        "to": "int"
    }
    """

    check_against_expected(lens, expected)


