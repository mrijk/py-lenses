# Selection of more complex use cases
from typing import Any, Iterator

from lenses.dict_item_lens import DictItemLens
from lenses.lens import ListLens
from lenses.more_itertools import first
from lenses.predefined import isnumeric, all_true, add
from lenses.predicate import Predicate
from lenses.transformer import Transformer


def test_complex_1():
    """ Check if all values are numeric """
    data = ["1", "2", "3"]

    lens_all = ListLens[str]()

    lens = lens_all >> isnumeric | all_true

    error, result = lens(data)

    assert not error
    assert result is True


def test_complex_2():
    """ Get all numeric values from a dictionary and sum them """

    data = {"x": 1, "y": 2, "z": 3}

    lens_dict = DictItemLens()
    second = Transformer[tuple, int](lambda x: x[1])

    lens = lens_dict >> second | add

    error, result = lens(data)

    assert not error
    assert result == 6


def test_complex_3():
    """ Log all data for which this is not a root key """

    # def check_root_key_mapping(payload: JSON) -> None:
    #     keys = (key for key in payload.keys() if "." in key)
    #
    #     for key in keys:
    #         root_key, rest = key.split(".", 1)
    #         if root_key not in NESTED_KEYS:
    #             logger.error("Root mapping of import has unknown top level keys.", error_root_key=root_key)

    NESTED_KEYS = ["classification", "destination", "extra", "feed", "malware", "source", "time", "protocol"]

    payload = {"source.ip": "127.0.0.1"}

    # Next lenses could be generalized
    with_dot = Predicate[str](f=lambda key: "." in key)
    unknown = Predicate[str](f=lambda key: key not in NESTED_KEYS)
    keys = Transformer[dict[str, Any], Iterator[str]](f=dict.keys)
    split = Transformer[str, list[str]](f=lambda s: s.split(".", 1))

    result = payload >> keys >> with_dot >> split >> first()  # >> unknown >> log

    print(list(result[1]))
