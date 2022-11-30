from lenses.generator import Generator
from lenses.more_itertools import sieve
from lenses.predefined import inc, add
from test.unit_tests.utils import check_against_expected


def test_generator():
    generator = Generator[int](f=lambda: range(5), can_throw=False)

    error, result = generator()
    assert not error
    assert list(result) == [0, 1, 2, 3, 4]


def test_compose():
    source = Generator[int](f=lambda: range(5), can_throw=False)

    generator = source >> inc

    error, result = generator()
    assert not error
    assert list(result) == [1, 2, 3, 4, 5]


def test_combine():
    source = Generator[int](f=lambda: range(5), can_throw=False)

    generator = source | add

    error, result = generator()
    assert not error
    assert result == 10


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
