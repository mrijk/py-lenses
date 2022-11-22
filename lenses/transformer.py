from typing import TypeVar, Callable

from lenses.lens import LensError, Lens

R = TypeVar('R')
S = TypeVar('S')


class Transformer(Lens[R, S]):
    def __init__(self, f: Callable[[R], S], can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, S | None]:
        if self.can_throw:
            try:
                result = self.f(data, **kwargs)
            except Exception as e:
                name = self.__class__.__name__
                return LensError(msg=f"{name} has thrown an exception", details=str(e)), None
            else:
                return None, result
        else:
            return None, self.f(data, **kwargs)

    def to_json(self) -> dict:
        type_0, type_1 = self.__orig_class__.__args__
        # TODO: add information about the function here
        return {
            "type": self.__class__.__name__,
            "from": type_0.__name__,
            "to": type_1.__name__,
            "can_throw": self.can_throw,
        }


class BaseTransformer(Lens[R, S]):
    def __init__(self, f):
        self.f = f

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, S | None]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                return self.f(data)
