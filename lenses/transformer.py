from typing import TypeVar

from lenses.lens import LensError, Lens

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')


class Transformer(Lens[R, S]):
    def __init__(self, f, can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, S | None]:
        if self.can_throw:
            try:
                result = self.f(data, **kwargs)
            except Exception as e:
                return LensError(msg="Transformer has thrown an exception", details=str(e)), None
            else:
                return None, result
        else:
            return None, self.f(data, **kwargs)


class BaseTransformer(Lens[R, S]):
    def __init__(self, f):
        self.f = f

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, S | None]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                return self.f(data)
