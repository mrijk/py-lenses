from typing import Any

import pytest as pytest

from lenses.key_lens import ListKeyLens
from lenses.lens import ListLens
from lenses.predefined import all_true, any_true, count, add, capitalize, reverse, lower, upper, swapcase, islower, \
    istitle, isupper, title, endswith, startswith, replace, removeprefix, removesuffix, to_list


def test_count():
    data = [1, 2, 3]

    error, result = count(data)

    assert not error
    assert result == 3


def test_add():
    data = [1, 2, 3]

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
        (removeprefix("th"), ["e", "quick", "brown", "fox"]),
        (removesuffix("ck"), ["the", "qui", "brown", "fox"]),
        (replace("o", "oo"), ["the", "quick", "broown", "foox"]),
        (reverse, ["eht", "kciuq", "nworb", "xof"]),
        (title, ["The", "Quick", "Brown", "Fox"]),
        (swapcase, ["THE", "QUICK", "BROWN", "FOX"]),
    ]
)
def test_string_operators(transformer, expected):
    data = {"x": ["the", "quick", "brown", "fox"]}

    lens_x = ListKeyLens[dict, str](key="x")

    lens = lens_x >> transformer

    error, result = lens(data)

    assert not error
    assert result == expected


def test_multiple_operators():
    data = {"x": ["The", "quick", "brown", "fox"]}

    lens_x = ListKeyLens[dict, str](key="x")

    lens = lens_x >> lower >> reverse >> title

    error, result = lens(data)

    assert not error
    assert result == ["Eht", "Kciuq", "Nworb", "Xof"]


@pytest.mark.parametrize(
    "transformer, expected",
    [
        (endswith("ck"), [False, True, False, False]),
        (islower, [False, True, False, True]),
        (istitle, [False, False, True, False]),
        (isupper, [True, False, False, False]),
        (startswith("B"), [False, False, True, False])
    ]
)
def test_string_predicates(transformer, expected):
    data = {"x": ["THE", "quick", "Brown", "fox"]}

    lens_x = ListKeyLens[dict, str](key="x")

    lens = lens_x >> transformer

    error, result = lens(data)

    assert not error
    assert result == expected


def test_to_list():
    data = ("aap", "noot", "mies")

    all = ListLens[Any]()

    lens = all | to_list

    error, result = lens(data)

    assert not error
    assert result == ["aap", "noot", "mies"]



