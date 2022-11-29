from lenses.lens import ListLens, FlattenListLens
from lenses.more_itertools import one, only, nth, take, nth_or_last, first, last


def test_first():
    data = [13, 14]

    all = ListLens[int]()
    select_first = first()

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_first_no_default():
    data = []

    all = ListLens[int]()
    select_first = first()

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_first_with_default():
    data = []

    all = ListLens[int]()
    select_first = first(default=42)

    lens = all | select_first

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42


def test_last():
    data = [13, 14]

    all = ListLens[int]()
    select_last = last()

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14


def test_last_no_default():
    data = []

    all = ListLens[int]()
    select_last = last()

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_last_with_default():
    data = []

    all = ListLens[int]()
    select_last = last(default=42)

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42


def test_one():
    data = [13]

    all = ListLens[int]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_one_too_short():
    data = []

    all = ListLens[dict]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_one_too_long():
    data = [13, 14]

    all = ListLens[int]()
    select_one = one()

    lens = all | select_one

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert error


def test_only():
    data = [13]

    all = ListLens[int]()
    select_only = only()

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 13


def test_only_no_default():
    data = []

    all = ListLens[int]()
    select_only = only()

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result is None


def test_only_with_default():
    data = []

    all = ListLens[int]()
    select_only = only(default=42)

    lens = all | select_only

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 42


def test_nth():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth(n=1)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14


def test_nth_with_default():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth(n=13, default=666)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 666


def test_nth_or_last():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_second = nth_or_last(n=1)

    lens = all | select_second

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 14


def test_nth_or_last_return_last():
    data = [13, 14, 15]

    all = ListLens[int]()
    select_last = nth_or_last(n=13)

    lens = all | select_last

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == 15


def test_take():
    data = [13, 14, 15]

    all = ListLens[int]()
    take_two = take(n=2)

    lens = all | take_two

    assert isinstance(lens, FlattenListLens)

    error, result = lens(data)
    assert not error
    assert result == [13, 14]