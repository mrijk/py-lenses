from typing import TypeVar, Callable, Iterable, Generic

from lenses.lens import LensError

T = TypeVar("T")


class Generator(Generic[T]):
    def __init__(self, f: Callable[[], Iterable[T]], can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

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