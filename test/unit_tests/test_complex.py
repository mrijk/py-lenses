# Selection of more complex use cases

from lenses.dict_item_lens import DictItemLens
from lenses.lens import ListLens
from lenses.predefined import isnumeric, all_true, add
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
    pass
