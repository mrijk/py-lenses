from typing import TypeVar

from lenses.lens import LensError, Lens, ComposedListLens
from lenses.transformer import BaseTransformer

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class KeyLens(BaseTransformer[R, S]):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f=self.get_by_key)

    def get_by_key(self, x: R) -> tuple[LensError | None, S | None]:
        match x:
            case None:
                return None, None
            case _:
                try:
                    return None, x[self.key]
                except KeyError:
                    return LensError(msg=f"Field {self.key} missing in {x}", key=self.key), None


class ListKeyLens(Lens[R, S]):
    def __init__(self, key: str):
        self.key_lens = KeyLens(key=key)
        self.key = key

    def __or__(self, other: "Lens[S, T]") -> "ComposedListKeyLens[R, T]":
        return ComposedListKeyLens[R, T](KeyLens(self.key), other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        return self.key_lens(data)


class ComposedListKeyLens(Lens[R, T]):
    def __init__(self, source: Lens, lens: Lens[S, T]):
        self.source = source
        self.lens = lens

    def __or__(self: Lens[R, T], other: "Lens[T, U]") -> "ComposedListKeyLens[R, U]":
        return ComposedListKeyLens[R, T](self, lens=other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        _, foo = self.source(data)
        result = (self.lens(v) for v in foo)

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, list(values)
