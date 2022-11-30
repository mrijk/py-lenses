from lenses.more_itertools import polynomial_from_roots


def test_polynomial_from_roots():
    roots = [5, -4, 3]
    polynomial = polynomial_from_roots(roots)

    error, result = polynomial()
    assert not error
    assert list(result) == [1, -4, -17, 60]
