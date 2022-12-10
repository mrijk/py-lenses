from abc import abstractmethod
from typing import Generator, Generic, Iterable, TypeVar, overload

from lenses.lens_result import LensResult, LensError, LensValue

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")
S1 = TypeVar("S1")
S2 = TypeVar("S2")
S3 = TypeVar("S3")
S4 = TypeVar("S4")
U = TypeVar("U")


class Lens(Generic[R, S]):
    def __or__(self, other: "Lens[S, T]") -> "ComposedLens[R, T]":
        return ComposedLens(self, other)

    def __rshift__(self, other: "Lens[S, T]") -> "ComposedLens[R, T]":
        return ComposedLens(self, other)

    def __add__(self, other: "Lens[R, S2]") -> "Combined2Lens[R, tuple[S, S2]]":
        return Combined2Lens(lens1=self, lens2=other)

    @abstractmethod
    def __call__(self, data: R, **kwargs):
        ...

    def to_json(self) -> dict:
        return {"type": self.__class__.__name__}


def combine(result: Generator) -> LensResult[tuple]:
    errors, values = list(zip(*result))

    errors = [error for error in errors if error]
    if errors:
        return LensError(msg="Failed to combine lenses", details=errors)
    else:
        return LensValue(tuple(values))


class CombinedLens(Lens[R, S]):
    def __init__(self, lenses):
        self.lenses = lenses

    def to_json(self) -> dict:
        lenses = [lens.to_json() for lens in self.lenses]
        from_type = lenses[0]["from"]
        to = (lens["to"] for lens in lenses)

        return {
            "type": self.__class__.__name__,
            "from": from_type,
            "to": "tuple[" + ", ".join(to) + "]",
            "lenses": lenses,
        }

    def __call__(self, data: R, **kwargs):
        result = (lens(data) for lens in self.lenses)

        return combine(result)


class Combined4Lens(CombinedLens[R, S]):
    def __init__(
        self,
        lens1: Lens[R, S1],
        lens2: Lens[R, S2],
        lens3: Lens[R, S3],
        lens4: Lens[R, S4],
    ):
        super().__init__([lens1, lens2, lens3, lens4])

    # @overload
    # def __rrshift__(self, other: tuple[LensError | None, R | None]) -> tuple[LensError | None, S | None]: ...
    #
    # @overload
    # def __rrshift__(self, other: R) -> tuple[LensError | None, S | None]: ...

    def __rrshift__(self: "Combined4Lens[R, tuple[S1, S2, S3, S4]]", other):
        match other:
            case tuple():
                # TODO: error handling
                return self(other[1])
            case _:
                return self(other)

    def __call__(self: Lens[R, tuple[S1, S2, S3, S4]], data: R, **kwargs) -> LensResult[tuple[S1, S2, S3, S4]]:
        return super().__call__(data, **kwargs)


class Combined3Lens(CombinedLens[R, S]):
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2], lens3: Lens[R, S3]):
        super().__init__([lens1, lens2, lens3])

    def __add__(
        self: Lens[R, tuple[S1, S2, S3]], other: Lens[R, S4]
    ) -> "Combined4Lens[R, tuple[S1, S2, S3, S4]]":
        return Combined4Lens(*self.lenses, lens4=other)

    @overload
    def __rrshift__(self, other: LensResult[R]) -> LensResult[S]: ...

    @overload
    def __rrshift__(self, other: R) -> LensResult[S]: ...

    def __rrshift__(self: "Combined3Lens[R, tuple[S1, S2, S3]]", other: R | LensResult[R]):
        match other:
            case tuple():
                # TODO: error handling
                return self(other[1])
            case _:
                return self(other)

    def __call__(self: Lens[R, tuple[S1, S2, S3]], data: R, **kwargs) -> LensResult[tuple[S1, S2, S3]]:
        return super().__call__(data, **kwargs)


class ComposedFlattenTupleLens(Lens[R, T]):
    def __init__(self, lens1: Lens, lens2: Lens[tuple, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self, data: R, **kwargs) -> LensResult[T]:
        _, source = self.lens1(data)
        return self.lens2(source)


class Combined2Lens(CombinedLens[R, S]):
    """lens = KeyLens(key="x") + KeyLens(key="y")."""

    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2]):
        self.lens1 = lens1
        self.lens2 = lens2
        super().__init__([lens1, lens2])

    def __or__(self, other: Lens[tuple[S1, S2], T]) -> ComposedFlattenTupleLens[R, T]:
        return ComposedFlattenTupleLens(lens1=self, lens2=other)

    def __rshift__(
        self: Lens[R, tuple[S1, S2]], other: "Lens[S1 | S2, T]"
    ) -> "ComposedTupleLens[R, tuple[T, T]]":
        return ComposedTupleLens(lens1=self, lens2=other)

    @overload
    def __rrshift__(self, other: tuple[LensError | None, R | None]) -> LensResult[S]: ...

    @overload
    def __rrshift__(self, other: R) -> LensResult[S]: ...

    def __rrshift__(self: "Combined2Lens[R, tuple[S1, S2]]", other):
        match other:
            case tuple():
                # TODO: error handling
                return self(other[1])
            case _:
                return self(other)

    def __add__(
        self: Lens[R, tuple[S1, S2]], other: Lens[R, S3]
    ) -> "Combined3Lens[R, tuple[S1, S2, S3]]":
        return Combined3Lens(*self.lenses, lens3=other)

    def __call__(self: Lens[R, tuple[S1, S2]], data: R, **kwargs) -> LensResult[tuple[S1, S2]]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                match self.lens1(data), self.lens2(data):
                    case LensValue(value1), LensValue(value2):
                        match self.lens1, self.lens2:
                            case Combined2Lens(), Combined2Lens():
                                return LensValue((*value1, *value2))
                            case Combined2Lens(), Lens():
                                return LensValue((*value1, value2))
                            case Lens(), Combined2Lens():
                                return LensValue((value1, *value2))
                            case Lens(), Lens():
                                return LensValue((value1, value2))
                    case LensError() as error, LensValue():
                        return error
                    case LensValue(), LensError() as error:
                        return error
                    case LensError() as error1, LensError() as error2:
                        return LensError(msg="Failed to combine lenses", details=[error1, error2])
                    case _:
                        return LensError(msg="tbd")


class ComposedLens(Lens[R, T]):
    """lens = KeyLens(key="x") >> KeyLens(key="y")."""

    def __init__(self, lens1: Lens[R, S], lens2: Lens[S, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    @overload
    def __rrshift__(self, other: LensResult[R]) -> LensResult[S]: ...

    @overload
    def __rrshift__(self, other: R) -> LensResult[S]: ...

    def __rrshift__(self, other):
        match other:
            case tuple():
                # TODO: error handling
                return self(other[1])
            case _:
                return self(other)

    def to_json(self) -> dict:
        lens1_json = self.lens1.to_json()
        lens2_json = self.lens2.to_json()

        return {
            "type": self.__class__.__name__,
            "from": lens1_json["from"],
            "to": lens2_json["to"],
            "lenses": [lens1_json, lens2_json],
        }

    def __call__(self, data: R, **kwargs) -> LensResult[T]:
        match data:
            case list() as l:
                return super().__call__(l, **kwargs)
            case _:
                match self.lens1(data):
                    case LensValue(value, kwargs):
                        return self.lens2(value, **kwargs)
                    case LensValue(value):
                        return self.lens2(value)
                    case LensError() as error:
                        return error, None


class ComposedListLens(Lens[R, S]):
    def __init__(self, lens: Lens[R, S]):
        self.lens = lens

    def __or__(self, other: Lens[Iterable[S], T]) -> "FlattenListLens[R, T]":
        return FlattenListLens[R, S](source=self, lens=other)

    def __call__(self, data: list[R], **kwargs) -> LensResult[list[S]]:
        result = (self.lens(v) for v in data)

        if any(isinstance(v, LensError) for v in result):
            return LensError(msg="Error in list")
        else:
            return LensValue(list(v.value() for v in result))


class FlattenListLens(Lens[R, S]):
    def __init__(self, source: Lens[R, R], lens: Lens[Iterable[R], S]):
        self.source = source
        self.lens = lens

    def __call__(self, data: Iterable[R], **kwargs) -> LensResult[S]:
        result = self.source(data)
        return self.lens(result)

    def to_json(self) -> dict:
        source_json = self.source.to_json()
        lens_json = self.lens.to_json()
        return {
            "type": self.__class__.__name__,
            "from": source_json["from"],
            "to": lens_json["to"],
        }


class ListLens(Generic[R], Lens[R, R]):
    def __rshift__(self, other: Lens[Iterable[R], S]) -> ComposedListLens[R, S]:
        return ComposedListLens[R, S](lens=other)

    def __or__(self, other: Lens[Iterable[R], S]) -> FlattenListLens[R, S]:
        return FlattenListLens[R, S](source=self, lens=other)

    def __call__(self, data: list[R], **kwargs) -> LensResult[list[R]]:
        return data

    def to_json(self) -> dict:
        args = self.__orig_class__.__args__
        type = args[0].__name__

        return {
            "type": self.__class__.__name__,
            "from": f"list[{type}]",
            "to": f"list[{type}]",
        }


class ComposedTupleLens(Lens[R, tuple[S1, S2]]):
    def __init__(self, lens1: Lens[R, tuple[S1, S2]], lens2: Lens[T, S1 | S2]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(
        self: "ComposedTupleLens[R, tuple[S1, S2]]", data: R, **kwargs
    ) -> LensResult[tuple[S1, S2]]:
        result = self.lens1(data)
        # TODO: add error handling

        result = (self.lens2(v) for v in result.value())

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list")
        else:
            return LensValue(tuple(values))
