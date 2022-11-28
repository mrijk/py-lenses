from more_itertools import one as mi_one
from typing import Iterable, TypeVar

from lenses.transformer import Transformer

T = TypeVar("T")


def one() -> Transformer[Iterable[T], T]:
    return Transformer(mi_one, can_throw=True)
