from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any

S = TypeVar("S")


class LensResult(Generic[S], ABC):
    @abstractmethod
    def value(self) -> S: ...

    def __rshift__(self, other) -> S:
        return self.value()


@dataclass
class LensError(LensResult[S]):
    def value(self) -> S:
        raise ValueError("No value available")

    msg: str
    key: str | None = None
    details: Any | None = None


@dataclass
class Value(Generic[S]):
    def __call__(self, *args, **kwargs) -> S:
        return 42  # TODO fix me!


value = Value()


@dataclass
class LensValue(Generic[S], LensResult[S]):
    _value: S

    def __init__(self, value: S):
        self._value = value

    def __rshift__(self, other: Value[S]):
        return other()

    def value(self) -> S:
        return self._value
