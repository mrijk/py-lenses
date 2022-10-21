from lenses.key_lens import KeyLens


def test_added_lenses():
    data = {"x": 42, "y": "42"}

    lens_x = KeyLens[dict, int](key="x")
    lens_y = KeyLens[dict, str](key="y")

    lens = lens_x + lens_y

    error, result = lens(data)

    assert not error
    assert result == (42, "42")


def test_added_lenses_with_missing_keys():
    data = {"x": 42, "y": "42"}

    lens_x = KeyLens[dict, int](key="a")
    lens_y = KeyLens[dict, str](key="b")

    lens = lens_x + lens_y

    error, result = lens(data)

    assert error
    error1, error2 = error.details
    assert error1.key == 'a'
    assert error2.key == 'b'

    assert result is None


def test_2_added_lenses():
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


def test_3_added_lenses():
    data = {"x": {"y": 42, "z": {"q": 666}, "w": 13}}

    lens_x = KeyLens[dict, dict](key="x")
    lens_y = KeyLens[dict, int](key="y")
    lens_z = KeyLens[dict, dict](key="z")
    lens_q = KeyLens[dict, int](key="q")
    lens_w = KeyLens(key="w")

    lens_yqw = lens_y + (lens_z >> lens_q) + lens_w

    lens = lens_x >> lens_yqw

    error, result = lens(data)

    assert not error
    assert result == (42, 666, 13)
