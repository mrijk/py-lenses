from typing import TypeVar, overload, Iterator

from lenses.lens import LensError
from lenses.transformer import Transformer

R = TypeVar("R")


class Predicate(Transformer[R, bool]):
    def __rrshift__(self, other: tuple[LensError | None, Iterator[R] | None]) -> tuple[LensError | None, Iterator[R] | None]:
        return None, (item for item in other[1] if self.f(item))

    def to_json(self) -> dict:
        type = self.__orig_class__.__args__
        # TODO: add information about the function here
        return {
            "type": self.__class__.__name__,
            "from": type[0].__name__,
            "to": "bool",
            "can_throw": self.can_throw,
        }
