import json

from lenses.key_lens import DictLens


def test_key_lens_to_json():
    lens = DictLens[int](key="x")

    result = lens.to_json()

    expected = """
    {
        "type": "KeyLens", 
        "from": "dict", 
        "to": "int", 
        "key": "x"
    }
    """

    assert json.loads(json.dumps(result)) == json.loads(expected)


def test_combined_2_lens_to_json():
    lens_x = DictLens[int](key="x")
    lens_y = DictLens[int](key="y")

    lens = lens_x + lens_y

    result = lens.to_json()

    expected = """
    {
        "type": "CombinedLens",
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

    assert json.loads(json.dumps(result)) == json.loads(expected)


def test_combined_3_lens_to_json():
    lens_x = DictLens[int](key="x")
    lens_y = DictLens[float](key="y")
    lens_z = DictLens[str](key="z")

    lens = lens_x + lens_y + lens_z

    result = lens.to_json()

    expected = """
    {
        "type": "Combined3Lens",
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

    assert json.loads(json.dumps(result)) == json.loads(expected)

