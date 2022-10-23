from lenses.key_lens import ListKeyLens
from lenses.predefined import all_true, any_true


def test_all_true():
    data = {"x": [True, True]}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | all_true

    error, result = lens(data)

    assert not error
    assert result is True


def test_any_false():
    data = {"x": [True, False]}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | all_true

    error, result = lens(data)

    assert not error
    assert result is False


def test_any_true():
    data = {"x": [True, True]}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | any_true

    error, result = lens(data)

    assert not error
    assert result is True


def test_none_true():
    data = {"x": [False, False]}

    lens_x = ListKeyLens[dict, bool](key="x")

    lens = lens_x | any_true

    error, result = lens(data)

    assert not error
    assert result is False
