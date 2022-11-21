from typing import TypeVar

from lenses.lens import LensError, Lens, ComposedTupleLens

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class ComposedGenericTupleLens(Lens[R, tuple]):
    def __init__(self, lens1: Lens[R, tuple], lens2: Lens[T, tuple]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self: "ComposedTupleLens[R, tuple", data: R, **kwargs) -> tuple[LensError | None, tuple | None]:
        errors, values = self.lens1(data)
        # TODO: add error handling

        result = (self.lens2(v) for v in values)

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, tuple(values)


class DictItemLens(Lens):
    def __call__(self, data: dict, **kwargs) -> tuple[LensError | None, list[tuple] | None]:
        return None, list(data.items())

    def __rshift__(self, other):
        return ComposedGenericTupleLens[R](lens1=self, lens2=other)
