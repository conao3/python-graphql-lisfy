from __future__ import annotations

import enum
from typing import Any, Optional


import pydantic


## Exceptions

class LisfyError(Exception):
    pass


class ReaderError(LisfyError):
    pass


## Enums

class OperationTypeEnum(enum.Enum):
    QUERY = enum.auto()
    MUTATION = enum.auto()
    SUBSCRIPTION = enum.auto()


## Values

class Value(pydantic.BaseModel):
    def lisfy(self, minify: bool=False) -> str:
        # raise NotImplementedError
        return str(self)


class Atom(Value):
    pass


class Int(Atom):
    value: int


class Float(Atom):
    value: float


class String(Atom):
    value: str


class Boolean(Atom):
    value: bool


class Null(Atom):
    pass


class Enum(Atom):
    value: str


class List(Atom):
    value: list[Atom]


class Object(Atom):
    value: dict[str, Atom]


class Type_(Value):
    type_: str
    is_list: bool = False
    is_non_null: bool = False


class VariableDefinition(Value):
    name: str
    type_: Type_
    default: Optional[Value] = None
    directives: list[Directive] = []


class VariableType(Value):
    type_: str
    is_list: bool = False
    is_non_null: bool = False


class Directive(Value):
    pass


class Selection(Value):
    pass


class Field(Selection):
    alias: Optional[str]
    name: str
    arguments: Optional[dict[str, str]]
    directives: Optional[list[Directive]]


class Definition(Value):
    pass


class ExecutableDefinition(Definition):
    pass


class OperationDefinition(ExecutableDefinition):
    type_: OperationTypeEnum
    name: Optional[str] = None
    variable_definitions: list[VariableDefinition] = []
    directives: list[Directive] = []
    selection_set: list[Selection]


class Document(Value):
    value: list[Definition]
