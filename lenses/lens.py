from dataclasses import dataclass
from typing import Generic, TypeVar, Any, Generator

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
S1 = TypeVar('S1')
S2 = TypeVar('S2')
S3 = TypeVar('S3')
S4 = TypeVar('S4')
U = TypeVar('U')


@dataclass
class LensError:
    msg: str
    key: str | None = None
    details: Any | None = None


class Lens(Generic[R, S]):
    def __call__(self, data: R | list[R], **kwargs) -> tuple[LensError | None, S | None]:
        pass

    def __or__(self, other: "Lens[S, T]") -> "Lens[R, T]":
        return ComposedLens[R, T](self, other)

    def __rshift__(self, other: "Lens[S, T]") -> "Lens[R, T]":
        return ComposedLens[R, T](self, other)

    def __add__(self, other: "Lens[R, S2]") -> "CombinedLens[R, tuple[S, S2]]":
        return CombinedLens(lens1=self, lens2=other)

    def to_json(self) -> dict:
        pass


def combine(result: Generator) -> tuple[LensError | None, tuple | None]:
    errors, values = list(zip(*result))

    errors = [error for error in errors if error]
    if errors:
        return LensError(msg="Failed to combine lenses", details=errors), None
    else:
        return None, tuple(values)


class Combined4Lens(Lens[R, tuple[S1, S2, S3, S4]]):
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2], lens3: Lens[R, S3], lens4: Lens[R, S4]):
        self.lens1 = lens1
        self.lens2 = lens2
        self.lens3 = lens3
        self.lens4 = lens4

    def __call__(self: Lens[R, tuple[S1, S2, S3, S4]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2, S3, S4] | None]:
        result = (lens(data) for lens in [self.lens1, self.lens2, self.lens3, self.lens4])

        return combine(result)


class Combined3Lens(Lens[R, tuple[S1, S2, S3]]):
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2], lens3: Lens[R, S3]):
        self.lens1 = lens1
        self.lens2 = lens2
        self.lens3 = lens3

    def to_json(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "lenses": [self.lens1.to_json(), self.lens2.to_json(), self.lens3.to_json()],
        }

    def __add__(self: Lens[R, tuple[S1, S2, S3]], other: Lens[R, S4]) -> "Combined4Lens[R, tuple[S1, S2, S3, S4]]":
        return Combined4Lens(lens1=self.lens1, lens2=self.lens2, lens3=self.lens3, lens4=other)

    def __call__(self: Lens[R, tuple[S1, S2, S3]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2, S3] | None]:
        result = (lens(data) for lens in [self.lens1, self.lens2, self.lens3])

        return combine(result)


class ComposedFlattenTupleLens(Lens[R, T]):
    def __init__(self, lens1: Lens, lens2: Lens[tuple, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        _, source = self.lens1(data)
        return self.lens2(source)


class CombinedLens(Lens[R, tuple[S1, S2]]):
    """lens = KeyLens(key="x") + KeyLens(key="y")"""
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2]):
        self.lens1 = lens1
        self.lens2 = lens2

    def to_json(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "lenses": [self.lens1.to_json(), self.lens2.to_json()],
        }

    def __or__(self, other: Lens[tuple[S1, S2], T]) -> ComposedFlattenTupleLens[R, T]:
        return ComposedFlattenTupleLens(lens1=self, lens2=other)

    def __rshift__(self: Lens[R, tuple[S1, S2]], other: "Lens[S1 | S2, T]") -> "ComposedTupleLens[R, tuple[T, T]]":
        return ComposedTupleLens(lens1=self, lens2=other)

    def __add__(self: Lens[R, tuple[S1, S2]], other: Lens[R, S3]) -> "Combined3Lens[R, tuple[S1, S2, S3]]":
        return Combined3Lens(lens1=self.lens1, lens2=self.lens2, lens3=other)

    def __call__(self: Lens[R, tuple[S1, S2]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2] | None]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                match self.lens1(data), self.lens2(data):
                    case (None, value1), (None, value2):
                        match self.lens1, self.lens2:
                            case CombinedLens(), CombinedLens():
                                return None, (*value1, *value2)
                            case CombinedLens(), Lens():
                                return None, (*value1, value2)
                            case Lens(), CombinedLens():
                                return None, (value1, *value2)
                            case Lens(), Lens():
                                return None, (value1, value2)
                    case (error, _), (None, _):
                        return error, None
                    case (None, _), (error, _):
                        return error, None
                    case (error1, _), (error2, _):
                        return LensError(msg="Failed to combine lenses", details=[error1, error2]), None
                    case _:
                        return LensError(msg="tbd"), None


class ComposedLens(Lens[R, T]):
    """lens = KeyLens(key="x") >> KeyLens(key="y")"""
    def __init__(self, lens1: Lens[R, S], lens2: Lens[S, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                match self.lens1(data):
                    case None, (value, kwargs):
                        return self.lens2(value, **kwargs)
                    case None, value:
                        return self.lens2(value)
                    case error, None:
                        return error, None


class ListLens(Lens[R, R]):
    def __or__(self, other: "Lens[S, T]") -> "Lens[list[R], list[T]]":
        return ComposedListLens[R, S](lens=other)

    def __call__(self, data: list[R], **kwargs) -> tuple[LensError | None, list[R] | None]:
        return None, data


class ComposedTupleLens(Lens[R, tuple[S1, S2]]):
    def __init__(self, lens1: Lens[R, tuple[S1, S2]], lens2: Lens[T, S1 | S2]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self: "ComposedTupleLens[R, tuple[S1, S2]]", data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2] | None]:
        errors, values = self.lens1(data)
        # TODO: add error handling

        result = (self.lens2(v) for v in values)

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, tuple(values)


class ComposedListLens(Lens[list[R], list[S]]):
    def __init__(self, lens: Lens[R, S]):
        self.lens = lens

    def __call__(self, data: list[R], **kwargs) -> tuple[LensError | None, list[S] | None]:
        result = (self.lens(v) for v in data)
        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, list(values)
