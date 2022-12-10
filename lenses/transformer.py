from typing import Callable, TypeVar, overload, Iterator

from lenses.lens import Lens
from lenses.lens_result import LensResult, LensError, LensValue

R = TypeVar("R")
S = TypeVar("S")


class Transformer(Lens[R, S]):
    def __init__(self, f: Callable[[R], S], can_throw: bool = False):
        self.f = f
        self.can_throw = can_throw

    @overload
    def __rrshift__(self, other: LensResult[R]) -> LensResult[S]: ...

    @overload
    def __rrshift__(self, other: list[R]) -> LensResult[S]: ...

    def __rrshift__(self: "Transformer[R, S]", other: R | list[R] | LensResult[R]):
        match other:
            case LensValue(x):
                # TODO: error handling
                if isinstance(x, Iterator):
                    return None, (self(item) for item in x)
                else:
                    return self(other[1])
            case _:
                return self(other)

    def __call__(self, data: R, **kwargs) -> LensResult[S]:
        if self.can_throw:
            try:
                result = self.f(data, **kwargs)
            except Exception as e:
                name = self.__class__.__name__
                return LensError(msg=f"{name} has thrown an exception", details=str(e))
            else:
                return LensValue(result)
        else:
            return LensValue(self.f(data, **kwargs))

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

    @overload
    def __rrshift__(self, other: LensResult[R]) -> LensResult[S]: ...

    @overload
    def __rrshift__(self, other: R) -> LensResult[S]: ...

    def __rrshift__(self: "BaseTransformer[R, S]", other) -> LensResult[S]:
        match other:
            case LensValue(x):
                return self(x)
            case _:
                return self(other)

    def __call__(self: "BaseTransformer[R, S]", data: R, **kwargs) -> LensResult[S]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                return self.f(data)
