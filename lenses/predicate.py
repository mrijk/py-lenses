from typing import TypeVar

from lenses.lens import Lens, LensError

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class Predicate(Lens[R, bool]):
    def __init__(self, f, can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, bool | None]:
        if self.can_throw:
            try:
                return None, self.f(data)
            except Exception as exc:
                return LensError(msg="Predicate has raised an exception", details=str(exc)), None
        else:
            return None, self.f(data)

    def to_json(self) -> dict:
        type = self.__orig_class__.__args__
        # TODO: add information about the function here
        return {
            "type": self.__class__.__name__,
            "from": type[0].__name__,
            "to": "bool",
        }
