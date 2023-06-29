from __future__ import annotations


import pydantic


## Exceptions

class LisfyError(Exception):
    pass


class ReaderError(LisfyError):
    pass


## Values

class Value(pydantic.BaseModel):
    def lisfy(self, minify: bool=False) -> str:
        # raise NotImplementedError
        return str(self)
