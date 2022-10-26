from lenses.key_lens import KeyLens
from lenses.lens import CombinedLens, Combined3Lens


def test_2_added_lenses():
    data = {"x": 42, "y": "42"}

    lens_x = KeyLens[dict, int](key="x")
    lens_y = KeyLens[dict, str](key="y")

    lens = lens_x + lens_y

    assert isinstance(lens, CombinedLens)

    error, result = lens(data)

    assert not error
    assert result == (42, "42")


def test_3_added_lenses():
    data = {"x": 42, "y": "42", "z": 3.14}

    lens_x = KeyLens[dict, int](key="x")
    lens_y = KeyLens[dict, str](key="y")
    lens_z = KeyLens[dict, float](key="z")

    lens = lens_x + lens_y + lens_z

    assert isinstance(lens, Combined3Lens)

    error, result = lens(data)

    assert not error
    assert result == (42, "42", 3.14)


def test_added_lenses_with_missing_keys():
    data = {"x": 42, "y": "42"}

    lens_x = KeyLens[dict, int](key="a")
    lens_y = KeyLens[dict, str](key="b")

    lens = lens_x + lens_y

    assert isinstance(lens, CombinedLens)

    error, result = lens(data)

    assert error
    error1, error2 = error.details
    assert error1.key == 'a'
    assert error2.key == 'b'

    assert result is None


def test_2_added_lenses_with_composition():
    data = {"x": {"y": 42, "z": {"q": 666}}}

    lens_x = KeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")
    lens_z = KeyLens[dict, dict](key="z")
    lens_q = lens_z >> KeyLens[dict, int](key="q")

    lens_yq = lens_y + lens_q

    lens = lens_x >> lens_yq

    error, result = lens(data)

    assert not error
    assert result == (42, 666)


def test_3_added_lenses_with_composition():
    data = {"x": {"y": 42, "z": {"q": 666}, "w": 13}}

    lens_x = KeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")
    lens_z = KeyLens[dict, dict](key="z")
    lens_q = KeyLens[dict, int](key="q")
    lens_w = KeyLens[dict, int](key="w")

    lens_yqw = lens_y + (lens_z >> lens_q) + lens_w

    assert isinstance(lens_yqw, Combined3Lens)

    lens = lens_x >> lens_yqw

    error, result = lens(data)

    assert not error
    assert result == (42, 666, 13)
