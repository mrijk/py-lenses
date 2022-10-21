from dataclasses import dataclass
from typing import Generic, TypeVar, Any, overload

R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
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

    def __add__(self, other: "Lens[R, T]") -> "Lens[R, tuple[S, T]]":
        return CombinedLens(self, other)


class CombinedLens(Lens[R, tuple[S, T]]):
    """lens = KeyLens(key="x") + KeyLens(key="y")"""
    def __init__(self, lens1: Lens[R, S], lens2: Lens[R, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, tuple[S, T] | None]:
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
    """lens = KeyLens(key="x") | KeyLens(key="y")"""
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
