from typing import TypeVar, Iterable

from lenses.predicate import Predicate
from lenses.transformer import Transformer

# Some predefined lenses

T = TypeVar('T')

add = Transformer[Iterable[int], int](sum, can_throw=True)

to_list = Transformer[Iterable, list](list)

count = Transformer[Iterable[T], int](len)

inc = Transformer[int, int](lambda x: x + 1)

dec = Transformer[int, int](lambda x: x - 1)

# String operators

capitalize = Transformer[str, str](str.capitalize)

upper = Transformer[str, str](str.upper)

lower = Transformer[str, str](str.lower)

reverse = Transformer[str, str](lambda s: s[::-1])

swapcase = Transformer[str, str](str.swapcase)

title = Transformer[str, str](str.title)

# String predicates


def endswith(prefix: str) -> Transformer[str, bool]:
    return Transformer[str, bool](lambda s: s.endswith(prefix))


def startswith(prefix: str) -> Transformer[str, bool]:
    return Transformer[str, bool](lambda s: s.startswith(prefix))


islower = Transformer[str, bool](str.islower)

istitle = Transformer[str, bool](str.istitle)

isupper = Transformer[str, bool](str.isupper)


def gt(value: T) -> Predicate[T]:
    return Predicate[T](lambda x: x > value)


all_true = Transformer[Iterable[bool], bool](all)

any_true = Transformer[Iterable[bool], bool](any)


# TODO: int should be T
not_none = Predicate[int | None](lambda x: x is not None)

