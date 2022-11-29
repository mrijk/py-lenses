from typing import Iterable, TypeVar

from lenses.transformer import Transformer

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U")


UNSET = object()


def first(default: T | None = UNSET) -> Transformer[Iterable[T], T]:
    from more_itertools import first
    if default == UNSET:
        return Transformer(lambda iterable: first(iterable), can_throw=True)
    else:
        return Transformer(lambda iterable: first(iterable, default=default), can_throw=False)


def last(default: T | None = UNSET) -> Transformer[Iterable[T], T]:
    from more_itertools import last
    if default == UNSET:
        return Transformer(lambda iterable: last(iterable), can_throw=True)
    else:
        return Transformer(lambda iterable: last(iterable, default=default), can_throw=False)


def one() -> Transformer[Iterable[T], T]:
    from more_itertools import one
    return Transformer(one, can_throw=True)


def only(default: T | None = UNSET) -> Transformer[Iterable[T], T]:
    from more_itertools import only
    if default == UNSET:
        return Transformer(lambda iterable: only(iterable), can_throw=True)
    else:
        return Transformer(lambda iterable: only(iterable, default=default), can_throw=True)


def nth(n: int, default: T | None = None) -> Transformer[Iterable[T], T | None]:
    from more_itertools import nth
    return Transformer(lambda iterable: nth(iterable, n=n, default=default))


def nth_or_last(n: int, default: T | None = None) -> Transformer[Iterable[T], T | None]:
    from more_itertools import nth_or_last
    return Transformer(lambda iterable: nth_or_last(iterable, n=n, default=default))


def take(n: int) -> Transformer[Iterable[R], list[S]]:
    from more_itertools import take
    return Transformer(lambda iterable: take(n, iterable))
