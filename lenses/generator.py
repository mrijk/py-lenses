from typing import TypeVar, Callable, Iterable, Generic

from lenses.lens import LensError
from lenses.transformer import Transformer

T = TypeVar("T")
U = TypeVar("U")


class Generator(Generic[T]):
    def __init__(self, f: Callable[[], Iterable[T]], can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    def __rshift__(self, other: Transformer[T, U]) -> "Generator[U]":
        can_throw = self.can_throw or other.can_throw
        return Generator(f=lambda: (other(value)[1] for value in self.f()), can_throw=can_throw)

    def __or__(self, other:  Transformer[Iterable[T], Iterable[U]]) -> "Generator[U]":
        return Generator(f=lambda: other(self.f())[1])

    def __add__(self, other: "Generator[U]") -> "Generator[tuple[T, U]]":
        # Todo: we need to use the same trick as combined lenses to have tuples of 2, 3, 4, etc. elements
        # Todo: error handling
        return Generator(f=lambda: zip(self.f(), other.f()))

    def __call__(self, **kwargs) -> tuple[LensError | None, Iterable[T] | None]:
        # TODO: add error handling
        return None, self.f()

    def to_json(self) -> dict:
        args = self.__orig_class__.__args__
        type = args[0].__name__

        return {
            "type": self.__class__.__name__,
            "to": f"Iterable[{type}]",
            "can_throw": self.can_throw,
        }