from typing import TypeVar, Iterable

from lenses.generator import Generator

T = TypeVar("T")


class count(Generator[T]):
    def __init__(self, start: T | None = None, step: T | None = None):
        from itertools import count

        match start, step:
            case None, None:
                super().__init__(f=lambda: count())
            case _, None:
                super().__init__(f=lambda: count(start=start))
            case None, _:
                super().__init__(f=lambda: count(step=step))
            case _, _:
                super().__init__(f=lambda: count(start=start, step=step))


class cycle(Generator[T]):
    def __init__(self, iterable: Iterable[T]):
        from itertools import cycle
        super().__init__(f=lambda: cycle(iterable))


class repeat(Generator[T]):
    def __init__(self, object: T, times: int | None = None):
        from itertools import repeat

        def _args():
            if times:
                yield times

        super().__init__(f=lambda: repeat(object, *_args()))


class chain(Generator[T]):
    def __init__(self, *iterables):
        from itertools import chain
        super().__init__(f=lambda: chain(*iterables))