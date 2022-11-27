from typing import Iterable, TypeVar, overload

from lenses.lens import ComposedLens, Lens, LensError
from lenses.predicate import Predicate
from lenses.transformer import BaseTransformer

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U")


class KeyLens(BaseTransformer[R, S]):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f=self.get_by_key)

    def to_json(self) -> dict:
        type_0, type_1 = self.__orig_class__.__args__
        return {
            "type": self.__class__.__name__,
            "from": type_0.__name__,
            "to": type_1.__name__,
            "key": self.key,
        }

    @overload
    def __rshift__(self, other: "ListKeyLens[S, T]") -> "FooListKeyLens[R, T]":
        ...

    @overload
    def __rshift__(self, other: "Lens[S, T]") -> "ComposedLens[R, T]":
        ...

    def __rshift__(self, other: Lens[S, T]) -> "ComposedLens[R, T]":
        if isinstance(other, ListKeyLens):
            return FooListKeyLens[R, T](self, other)
        else:
            return ComposedLens[R, T](self, other)

    def get_by_key(self, data: R) -> tuple[LensError | None, S | None]:
        match data:
            case None:
                return None, None
            case dict() if data is None:
                return None, None
            case _:
                try:
                    return None, data[self.key]
                except KeyError:
                    return (
                        LensError(
                            msg=f"Field {self.key} missing in {data}", key=self.key
                        ),
                        None,
                    )


class NullableKeyLens(KeyLens[R, S | None]):
    def get_by_key(self, data: R) -> tuple[LensError | None, S | None]:
        match data:
            case None:
                return None, None
            case dict() if data is None:
                return None, None
            case _:
                try:
                    return None, data[self.key]
                except KeyError:
                    return None, None

    def to_json(self) -> dict:
        type_0, type_1 = self.__orig_class__.__args__
        return {
            "type": self.__class__.__name__,
            "from": type_0.__name__,
            "to": f"{type_1.__name__} | None",
            "key": self.key,
        }


DictLens = KeyLens[dict, T]
NullableDictLens = NullableKeyLens[dict, T]


class ListKeyLens(Lens[R, S]):
    key_lens: KeyLens

    def __init__(self, key: str):
        self.key_lens = KeyLens(key=key)

    def __or__(self, other: Lens[Iterable[S], T]) -> "ComposedFlattenListKeyLens[R, T]":
        return ComposedFlattenListKeyLens[R, T](self.key_lens, other)

    @overload
    def __rshift__(
        self, other: NullableKeyLens[S, T]
    ) -> "ComposedListKeyLens[R, T | None]":
        ...

    def __rshift__(self, other: Lens[S, T]) -> "ComposedListKeyLens[R, T]":
        return ComposedListKeyLens[R, T](self.key_lens, other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        return self.key_lens(data)

    def to_json(self) -> dict:
        type_0, type_1 = self.__orig_class__.__args__
        return {
            "type": self.__class__.__name__,
            "from": f"list[{type_0.__name__}]",
            "to": f"list[{type_1.__name__}]",
            "key": self.key_lens.key,
        }


class FooListKeyLens(Lens[R, S]):
    def __init__(self, source: Lens, lens: ListKeyLens[T, U]):
        self.source = source
        self.lens = lens

    def __rshift__(self, other: Lens[S, T]) -> "ComposedListKeyLens[R, T]":
        return ComposedListKeyLens[R, T](self, other)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, list[S] | None]:
        errors, source = self.source(data)
        if errors:
            return errors, None

        return self.lens.key_lens(source)


class ComposedListKeyLens(Lens[R, S]):
    def __init__(self, source: Lens, lens: Lens[T, U]):
        self.source = source
        self.lens = lens

    def __rshift__(self, other: Lens[S, U]) -> "ComposedListKeyLens[R, U]":
        args = other.__orig_class__.__args__[0]
        if args.__subclasscheck__(list):
            return ComposedFlattenListKeyLens[R, U](self, lens=other)
        return ComposedListKeyLens[R, U](self, lens=other)

    def __or__(
        self: Lens[R, T], other: Lens[list[T], U]
    ) -> "ComposedFlattenListKeyLens[R, U]":
        return ComposedFlattenListKeyLens[R, U](self, lens=other)

    def __call__(
        self, data: R, **kwargs
    ) -> tuple[LensError | None, list[S | None] | None]:
        errors, source = self.source(data)
        if errors:
            return errors, None

        if isinstance(self.lens, Predicate):
            # TODO: better to return a different kind of lens in the __rshift__ when this is a predicate
            predicate_results = [(v, self.lens(v)) for v in source]
            result = ((p[0], v) for v, p in predicate_results if p[1] or p[0])
        else:
            result = [self.lens(v, **kwargs) for v in source]

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list", details=errors), None
        else:
            return None, list(values)

    def to_json(self) -> dict:
        lens_json = self.lens.to_json()
        return {
            "type": self.__class__.__name__,
            "from": lens_json["from"],
            "to": lens_json["to"],
            "lens": lens_json,
        }


class ComposedFlattenListKeyLens(ComposedListKeyLens[R, T]):
    def __init__(self, source: Lens, lens: Lens[T, U]):
        super().__init__(source, lens)

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        _, source = self.source(data)
        # TODO: add error handling

        return self.lens(source)
