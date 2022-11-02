from typing import TypeVar

from lenses.predicate import Predicate
from lenses.transformer import Transformer

# Some predefined lenses

T = TypeVar('T')

add = Transformer[list[T], T](sum, can_throw=True)

to_list = Transformer[tuple, list](list)

count = Transformer[list[T], int](len)

inc = Transformer[int, int](lambda x: x + 1)

dec = Transformer[int, int](lambda x: x - 1)

capitalize = Transformer[str, str](lambda s: s.capitalize())

reverse = Transformer[str, str](lambda s: s[::-1])


def gt(value: T) -> Predicate[T]:
    return Predicate[T](lambda x: x > value)


all_true = Transformer[list[bool], bool](all)

any_true = Transformer[list[bool], bool](any)

