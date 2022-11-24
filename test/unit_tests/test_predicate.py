import pytest as pytest

from lenses.predefined import gt
from lenses.predicate import Predicate
from test.unit_tests.utils import check_against_expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (13, False),
        (14, True),
     ])
def test_predicate(data, expected):
    gt_13 = gt(13)

    error, result = gt_13(data)

    assert not error
    assert result is expected


def test_predicate_with_raise():
    def failure(_: int) -> bool:
        raise ValueError("Oh no!")

    disaster = Predicate[int](failure, can_throw=True)

    error, result = disaster(13)

    assert error
    assert error.msg == "Predicate has thrown an exception"
    assert error.details == "Oh no!"


def test_predicate_to_json():
    # gt_13 = gt(13)
    gt_13 = Predicate[int](lambda x: x > 13)

    expected = """
    {
        "type": "Predicate",
        "from": "int",
        "to": "bool",
        "can_throw": false
    }
    """

    check_against_expected(gt_13, expected)