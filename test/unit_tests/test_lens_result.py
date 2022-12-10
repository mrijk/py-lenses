import pytest

from lenses.lens_result import LensError, LensValue, LensResult


def test_valid_result():
    result = LensValue(value=13)

    assert result.value() == 13


def test_no_value():
    result = LensError(msg="An error occurred")

    with pytest.raises(ValueError) as exc:
        _ = result.value()


def test_matching_valid_result():
    result: LensResult = LensValue(value=13)

    match result:
        case LensValue(x):
            assert x == 13
        case LensError():
            assert False, "Can't happen"


def test_matching_error():
    result = LensError(msg="An error occurred")

    match result:
        case LensValue(x):
            assert False, "Can't happen"
        case LensError(msg):
            assert msg == "An error occurred"


