from typing import TypeVar, Any, Iterable

from lenses.predicate import Predicate
from lenses.transformer import Transformer

# Some predefined lenses

T = TypeVar('T')

add = Transformer[Iterable[T], T](sum, can_throw=True)

to_list = Transformer[Iterable, list](list)

count = Transformer[Iterable[T], int](len)

inc = Transformer[int, int](lambda x: x + 1)

dec = Transformer[int, int](lambda x: x - 1)

# String operators

capitalize = Transformer[str, str](lambda s: s.capitalize())

upper = Transformer[str, str](lambda s: s.upper())

lower = Transformer[str, str](lambda s: s.lower())

reverse = Transformer[str, str](lambda s: s[::-1])


def gt(value: T) -> Predicate[T]:
    return Predicate[T](lambda x: x > value)


all_true = Transformer[Iterable[bool], bool](all)

any_true = Transformer[Iterable[bool], bool](any)


# TODO: int should be T
not_none = Predicate[int | None](lambda x: x is not None)

