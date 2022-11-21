from dataclasses import dataclass
from typing import Generic, TypeVar, Any, Generator, Iterable

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

    def __add__(self, other: "Lens[R, S2]") -> "Combined2Lens[R, tuple[S, S2]]":
        return Combined2Lens(lens1=self, lens2=other)

    def to_json(self) -> dict:
        pass


def combine(result: Generator) -> tuple[LensError | None, tuple | None]:
    errors, values = list(zip(*result))

    errors = [error for error in errors if error]
    if errors:
        return LensError(msg="Failed to combine lenses", details=errors), None
    else:
        return None, tuple(values)


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
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2], lens3: Lens[R, S3], lens4: Lens[R, S4]):
        super().__init__([lens1, lens2, lens3, lens4])

    def __call__(self: Lens[R, tuple[S1, S2, S3, S4]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2, S3, S4] | None]:
        return super().__call__(data, **kwargs)


class Combined3Lens(CombinedLens[R, S]):
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2], lens3: Lens[R, S3]):
        super().__init__([lens1, lens2, lens3])

    def __add__(self: Lens[R, tuple[S1, S2, S3]], other: Lens[R, S4]) -> "Combined4Lens[R, tuple[S1, S2, S3, S4]]":
        return Combined4Lens(*self.lenses, lens4=other)

    def __call__(self: Lens[R, tuple[S1, S2, S3]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2, S3] | None]:
        return super().__call__(data, **kwargs)


class ComposedFlattenTupleLens(Lens[R, T]):
    def __init__(self, lens1: Lens, lens2: Lens[tuple, T]):
        self.lens1 = lens1
        self.lens2 = lens2

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        _, source = self.lens1(data)
        return self.lens2(source)


class Combined2Lens(CombinedLens[R, S]):
    """lens = KeyLens(key="x") + KeyLens(key="y")"""
    def __init__(self, lens1: Lens[R, S1], lens2: Lens[R, S2]):
        self.lens1 = lens1
        self.lens2 = lens2
        super().__init__([lens1, lens2])

    def __or__(self, other: Lens[tuple[S1, S2], T]) -> ComposedFlattenTupleLens[R, T]:
        return ComposedFlattenTupleLens(lens1=self, lens2=other)

    def __rshift__(self: Lens[R, tuple[S1, S2]], other: "Lens[S1 | S2, T]") -> "ComposedTupleLens[R, tuple[T, T]]":
        return ComposedTupleLens(lens1=self, lens2=other)

    def __add__(self: Lens[R, tuple[S1, S2]], other: Lens[R, S3]) -> "Combined3Lens[R, tuple[S1, S2, S3]]":
        return Combined3Lens(*self.lenses, lens3=other)

    def __call__(self: Lens[R, tuple[S1, S2]], data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2] | None]:
        match data:
            case list() as l:
                return super().__call__(l)
            case _:
                match self.lens1(data), self.lens2(data):
                    case (None, value1), (None, value2):
                        match self.lens1, self.lens2:
                            case Combined2Lens(), Combined2Lens():
                                return None, (*value1, *value2)
                            case Combined2Lens(), Lens():
                                return None, (*value1, value2)
                            case Lens(), Combined2Lens():
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

    def to_json(self) -> dict:
        lens1_json = self.lens1.to_json()
        lens2_json = self.lens2.to_json()

        return {
            "type": self.__class__.__name__,
            "from": lens1_json["from"],
            "to": lens2_json["to"],
            "lenses": [lens1_json, lens2_json]
        }

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


class ComposedListLens(Lens[R, S]):
    def __init__(self, lens: Lens[R, S]):
        self.lens = lens

    def __or__(self, other: Lens[Iterable[S], T]) -> "FlattenListLens[R, T]":
        return FlattenListLens[R, S](source=self, lens=other)

    def __call__(self, data: list[R], **kwargs) -> tuple[LensError | None, list[S] | None]:
        result = (self.lens(v) for v in data)
        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, list(values)


class FlattenListLens(Lens[R, S]):
    def __init__(self, source: Lens[R, R],  lens: Lens[Iterable[R], S]):
        self.source = source
        self.lens = lens

    def __call__(self, data: Iterable[R], **kwargs) -> tuple[LensError | None, S | None]:
        error, result = self.source(data)
        return self.lens(result)

    def to_json(self) -> dict:
        source_json = self.source.to_json()
        lens_json = self.lens.to_json()
        return {
            "type": self.__class__.__name__,
            "from": source_json["from"],
            "to": lens_json["to"],
        }


class ListLens(Generic[R]):
    def __rshift__(self, other: Lens[Iterable[R], S]) -> ComposedListLens[R, S]:
        return ComposedListLens[R, S](lens=other)

    def __or__(self, other: Lens[Iterable[R], S]) -> FlattenListLens[R, S]:
        return FlattenListLens[R, S](source=self, lens=other)

    def __call__(self, data: list[R], **kwargs) -> tuple[LensError | None, list[R] | None]:
        return None, data

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

    def __call__(self: "ComposedTupleLens[R, tuple[S1, S2]]", data: R, **kwargs) -> tuple[LensError | None, tuple[S1, S2] | None]:
        errors, values = self.lens1(data)
        # TODO: add error handling

        result = (self.lens2(v) for v in values)

        errors, values = list(zip(*result))

        if any(errors):
            return LensError(msg="Error in list"), None
        else:
            return None, tuple(values)

