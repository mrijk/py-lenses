from typing import TypeVar

from lenses.transformer import Transformer

R = TypeVar('R')


class Predicate(Transformer[R, bool]):
    def to_json(self) -> dict:
        type = self.__orig_class__.__args__
        # TODO: add information about the function here
        return {
            "type": self.__class__.__name__,
            "from": type[0].__name__,
            "to": "bool",
            "can_throw": self.can_throw,
        }
