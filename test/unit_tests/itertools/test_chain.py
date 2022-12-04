from lenses.itertools import chain


def test_chain():
    generator = chain[int | str]("abc", [1, 2, 3])

    error, result = generator()

    assert not error
    assert list(result) == ["a", "b", "c", 1, 2, 3]