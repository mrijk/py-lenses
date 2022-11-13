from lenses.key_lens import KeyLens, ListKeyLens, ComposedListKeyLens, ComposedFlattenListKeyLens, DictLens
from lenses.lens import ListLens, ComposedListLens
from lenses.predefined import add, count, inc
from lenses.predicate import Predicate


def test_all():
    data = [{"x": 13}, {"x": 14}]

    all = ListLens[dict]()

    lens = all

    assert isinstance(lens, ListLens)

    error, result = lens(data)
    assert not error
    assert result == data


def test_list():
    data = [{"x": 13}, {"x": 14}]

    all = ListLens[dict]()
    lens_x = KeyLens[dict, int](key="x")

    lens = all | lens_x

    assert isinstance(lens, ComposedListLens)

    error, result = lens(data)

    assert not error
    assert result == [13, 14]


def test_plain_list():
    data = [{"x": 13, "y": 14}]

    all = ListLens[dict]()
    lens_x = KeyLens[dict, int](key="x")
    lens_y = KeyLens[dict, int](key="y")

    lens = all | (lens_x + lens_y)

    assert isinstance(lens, ComposedListLens)

    error, result = lens(data)

    assert not error
    assert result == [(13, 14)]


def test_list_key_lens():
    data = {"x": [{"y": 13}, {"y": 14}]}

    lens = ListKeyLens[dict, dict](key="x")

    assert isinstance(lens, ListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [{"y": 13}, {"y": 14}]


def test_list_in_dict():
    data = {"x": [{"y": 13}, {"y": 14}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")

    lens = lens_x >> lens_y

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [13, 14]


def test_list_in_dict_2():
    data = {"x": [{"y": {"z": 13}}, {"y": {"z": 14}}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, dict](key="y")
    lens_z = KeyLens[dict, int](key="z")

    lens = lens_x >> lens_y >> lens_z

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [13, 14]


def test_list_in_dict_3():
    data = {"x": [{"y": [{"z": 13}, {"z": 14}]}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = ListKeyLens[dict, dict](key="y")
    lens_z = KeyLens[dict, int](key="z")

    lens = lens_x >> (lens_y >> lens_z)

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [[13, 14]]


def test_aggregate_list():
    data = {"x": [{"y": {"z": 13}}, {"y": {"z": 14}}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, dict](key="y")
    lens_z = KeyLens[dict, int](key="z")

    lens = lens_x >> lens_y >> lens_z | add

    assert isinstance(lens, ComposedFlattenListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == 27


def test_filtered_list():
    """Count number of records for which y greater than 13"""
    data = {"x": [{"y": 13}, {"y": 14}]}

    lens_x = ListKeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")

    gt_13 = Predicate[int](lambda x: x > 13)

    lens = lens_x >> lens_y >> gt_13 | count

    error, result = lens(data)

    assert not error
    assert result == 1


def test_complex():
    """ Return all z values increased by 1 if z >= 14"""
    data = {"x": {"y": [{"z": 13}, {"z": 14}]}}

    lens_x = DictLens[dict](key="x")
    lens_y = ListKeyLens[dict, dict](key="y")
    lens_z = DictLens[int](key="z")
    gt_14  = Predicate[int](lambda x: x >= 14)

    lens = lens_x >> lens_y >> lens_z >> gt_14 >> inc

    assert isinstance(lens, ComposedListKeyLens)

    error, result = lens(data)

    assert not error
    assert result == [15]

