from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import tail


def test_tail():
    data = "ABCDEFG"

    all = ListLens[str]()
    last_three = tail(n=3)

    lens = all | last_three

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert list(result) == ['E', 'F', 'G']
