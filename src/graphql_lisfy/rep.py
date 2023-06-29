from typing import Optional

import more_itertools

from . import types
from . import reader


def read(x: str) -> Optional[types.Value]:
    stream = more_itertools.peekable(x)
    return reader.read(stream)


def eval(x: Optional[types.Value]) -> Optional[types.Value]:
    return x


def print(x: Optional[types.Value]) -> Optional[str]:
    if x is None:
        return None

    return x.lisfy()


def rep(x: str) -> Optional[str]:
    return print(eval(read(x)))
