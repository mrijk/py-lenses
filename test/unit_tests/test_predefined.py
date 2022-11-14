import pytest as pytest

from lenses.key_lens import ListKeyLens
from lenses.predefined import all_true, any_true, count, add, capitalize, reverse, lower, upper


def test_count():
    data = [1, 2, 3]

    error, result = count(data)

    assert not error
    assert result == 3


def test_add():
    data = [1, 2, 3]

    # TODO: incorrect result type shown.
    error, result = add(data)

    assert not error
    assert result == 6


@pytest.mark.parametrize(
    "values, expected",
    [
        ((True, True), True),
        ((True, False), False),
        ({True, True}, True),
        ({True, False}, False),
        ([True, True], True),
        ([True, False], False),
    ]
)
def test_all_true(values, expected):
    error, result = all_true(values)

    assert not error
    assert result is expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ([True, True], True),
        ([True, False], False),
    ]
)
def test_all_true_in_dict(values, expected):
    data = {"x": values}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | all_true

    error, result = lens(data)

    assert not error
    assert result is expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ([True, True], True),
        ([False, False], False),
    ]
)
def test_any_true(values, expected):
    data = {"x": values}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | any_true

    error, result = lens(data)

    assert not error
    assert result is expected


@pytest.mark.parametrize(
    "transformer, expected",
    [
        (capitalize, ["The", "Quick", "Brown", "Fox"]),
        (lower, ["the", "quick", "brown", "fox"]),
        (upper, ["THE", "QUICK", "BROWN", "FOX"]),
        (reverse, ["eht", "kciuq", "nworb", "xof"]),
    ]
)
def test_string_operators(transformer, expected):
    data = {"x": ["the", "quick", "brown", "fox"]}

    lens_x = ListKeyLens[dict, str](key="x")

    lens = lens_x >> transformer

    error, result = lens(data)

    assert not error
    assert result == expected