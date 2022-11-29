from typing import Iterable, TypeVar, Callable, Any, Optional

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


# TODO: probably better to have a Lens here instead of an optional Callable
def strictly_n(n: int, too_short: Optional[Callable] = None, too_long: Optional[Callable] = None) -> Transformer[
    Iterable[T], Iterable[T]]:
    from more_itertools import strictly_n
    can_throw = too_short is None or too_long is None
    return Transformer(lambda iterable: strictly_n(iterable, n=n, too_short=too_short, too_long=too_long),
                       can_throw=can_throw)


def nth(n: int, default: T | None = None) -> Transformer[Iterable[T], T | None]:
    from more_itertools import nth
    return Transformer(lambda iterable: nth(iterable, n=n, default=default))


def nth_or_last(n: int, default: T | None = None) -> Transformer[Iterable[T], T | None]:
    from more_itertools import nth_or_last
    return Transformer(lambda iterable: nth_or_last(iterable, n=n, default=default))


def lstrip(pred: Callable) -> Transformer[Iterable[T], Iterable[T]]:
    from more_itertools import lstrip
    return Transformer(lambda iterable: lstrip(iterable, pred))


def strip(pred: Callable) -> Transformer[Iterable[T], Iterable[T]]:
    from more_itertools import strip
    return Transformer(lambda iterable: strip(iterable, pred))


def rstrip(pred: Callable[[Any], bool]) -> Transformer[Iterable[Any], Iterable[Any]]:
    from more_itertools import rstrip
    return Transformer(lambda iterable: rstrip(iterable, pred))


def take(n: int) -> Transformer[Iterable[R], list[S]]:
    from more_itertools import take
    return Transformer(lambda iterable: take(n, iterable))


def tail(n: int) -> Transformer[Iterable[Any], Iterable[Any]]:
    from more_itertools import tail
    return Transformer(lambda iterable: tail(n, iterable))
