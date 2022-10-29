from typing import TypeVar, overload, get_args, Any

from lenses.lens import LensError, Lens, ComposedListLens, ComposedLens
from lenses.predicate import Predicate
from lenses.transformer import BaseTransformer, Transformer

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class KeyLens(BaseTransformer[R, S]):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f=self.get_by_key)

    def get_by_key(self, data: R) -> tuple[LensError | None, S | None]:
        match data:
            case None:
                return None, None
            case _:
                try:
                    return None, data[self.key]
                except KeyError:
                    return LensError(msg=f"Field {self.key} missing in {data}", key=self.key), None


DictLens = KeyLens[dict, T]


class ListKeyLens(Lens[R, S]):
    def __init__(self, key: str):
        self.key_lens = KeyLens(key=key)

    def __or__(self, other: Lens[list[S], T]) -> "ComposedFlattenListKeyLens[R, T]":
        return ComposedFlattenListKeyLens[R, T](self.key_lens, other)

    def __rshift__(self, other: Lens[S, T]) -> "ComposedListKeyLens[R, T]":
        return ComposedListKeyLens[R, T](self.key_lens, other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        return self.key_lens(data)


class ComposedListKeyLens(Lens[R, S]):
    def __init__(self, source: Lens, lens: Lens[T, U]):
        self.source = source
        self.lens = lens

    def __rshift__(self: Lens[R, S], other: Lens[S, U]) -> "ComposedListKeyLens[R, U]":
        args = other.__orig_class__.__args__[0]
        if args.__subclasscheck__(list):
            return ComposedFlattenListKeyLens[R, U](self, lens=other)
        return ComposedListKeyLens[R, U](self, lens=other)

    def __or__(self: Lens[R, T], other: Lens[list[T], U]) -> "ComposedFlattenListKeyLens[R, U]":
        return ComposedFlattenListKeyLens[R, U](self, lens=other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        errors, source = self.source(data)
        if errors:
            return errors, None

        if isinstance(self.lens, Predicate):
            # TODO: better to return a different kind of lens in the __rshift__ when this is a predicate
            predicate_results = [(v, self.lens(v)) for v in source]
            result = ((p[0], v) for v, p in predicate_results if p[1] or p[0])
        else:
            result = (self.lens(v) for v in source)

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list", details=errors), None
        else:
            return None, list(values)


class ComposedFlattenListKeyLens(ComposedListKeyLens[R, T]):
    def __init__(self, source: Lens, lens: Lens[T, U]):
        super().__init__(source, lens)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        _, source = self.source(data)
        # TODO: add error handling

        return self.lens(source)
