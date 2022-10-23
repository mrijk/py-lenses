from typing import TypeVar

from lenses.lens import Lens, LensError

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class Predicate(Lens[R, R]):
    def __init__(self, f, can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, bool | None]:
        return None, self.f(data)
