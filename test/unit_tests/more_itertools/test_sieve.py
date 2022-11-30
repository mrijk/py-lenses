from lenses.more_itertools import sieve


def test_sieve():
    primes = sieve(64)

    error, result = primes()
    assert not error
    assert list(result) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]