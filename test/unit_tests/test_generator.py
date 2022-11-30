from lenses.generator import Generator
from test.unit_tests.utils import check_against_expected


def test_generator():
    generator = Generator[int](f=lambda: range(5), can_throw=False)

    error, result = generator()
    assert not error
    assert list(result) == [0, 1, 2, 3, 4]


def test_generator_to_json():
    generator = Generator[int](f=lambda: range(5), can_throw=False)

    expected = """
    {
        "type": "Generator",
        "to": "Iterable[int]",
        "can_throw": false
    }
    """

    check_against_expected(generator, expected)
