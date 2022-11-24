from typing import TypeVar

from lenses.lens import Lens, LensError

R = TypeVar("R")
T = TypeVar("T")


class InjectLens(Lens[R, T]):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, data: R, **kwargs) -> tuple[LensError | None, T | None]:
        return None, (data, self.kwargs)

    def to_json(self) -> dict:
        args = {**self.kwargs}
        return {"type": self.__class__.__name__, "args": args}
