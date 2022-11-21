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


def removeprefix(prefix: str) -> Transformer[str, str]:
    return Transformer[str, str](lambda s: s.removeprefix(prefix))


def removesuffix(suffix: str) -> Transformer[str, str]:
    return Transformer[str, str](lambda s: s.removesuffix(suffix))


def replace(old: str, new: str) -> Transformer[str, str]:
    return Transformer[str, str](lambda s: s.replace(old, new))


reverse = Transformer[str, str](lambda s: s[::-1])


def strip(chars: str | None = None) -> Transformer[str, str]:
    return Transformer[str, str](lambda s: s.strip(chars))


swapcase = Transformer[str, str](str.swapcase)

title = Transformer[str, str](str.title)


def find(sub: str) -> Transformer[str, int]:
    return Transformer[str, int](lambda s: s.find(sub))


# String predicates


def endswith(prefix: str) -> Transformer[str, bool]:
    return Transformer[str, bool](lambda s: s.endswith(prefix))


def startswith(prefix: str) -> Transformer[str, bool]:
    return Transformer[str, bool](lambda s: s.startswith(prefix))


isidentifier = Transformer[str, bool](str.isidentifier)

islower = Transformer[str, bool](str.islower)

isnumeric = Transformer[str, bool](str.isnumeric)

isprintable = Transformer[str, bool](str.isprintable)

isspace = Transformer[str, bool](str.isspace)

istitle = Transformer[str, bool](str.istitle)

isupper = Transformer[str, bool](str.isupper)


def gt(value: T) -> Predicate[T]:
    return Predicate[T](lambda x: x > value)


all_true = Transformer[Iterable[bool], bool](all)

any_true = Transformer[Iterable[bool], bool](any)


# TODO: int should be T
not_none = Predicate[int | None](lambda x: x is not None)

