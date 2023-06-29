from __future__ import annotations
from typing import Any, Literal, Optional
import typing

import more_itertools

from . import types
from . import subr

PUNCTUATOR = '!$&()...:=@[]{|}'
LETTER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGIT = '0123456789'

@typing.overload
def read_name(input_stream: more_itertools.peekable[str], error_p: Literal[True] = True) -> str: ...

@typing.overload
def read_name(input_stream: more_itertools.peekable[str], error_p: Literal[False]) -> Optional[str]: ...

def read_name(input_stream: more_itertools.peekable[str], error_p: bool = True) -> Optional[str]:
    name_start = LETTER + '_'
    name_continue = LETTER + DIGIT + '_'

    peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

    if peek not in name_start:
        if error_p:
            raise types.ReaderError(f'Unexpected character: {peek}')
        return None

    return ''.join(subr.itertools.takewhile_inclusive(lambda x: x in name_continue, input_stream))


def read_type(input_stream: more_itertools.peekable[str]) -> types.Type_:
    peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

    is_list = False
    is_non_null = False

    if peek == '[':
        is_list = True
        subr.reader.ensure_char('[', input_stream)
        type_ = read_name(input_stream)
        subr.reader.ensure_char(']', input_stream)

    else:
        type_ = read_name(input_stream)

    peek = subr.reader.peek_char(True, input_stream, eof_error_p=False, eof_value='EOF', recursive_p=True)

    if peek == '!':
        is_non_null = True
        subr.reader.ensure_char('!', input_stream)

    return types.Type_(
        type_=type_,
        is_list=is_list,
        is_non_null=is_non_null,
    )


def read_atom(input_stream: more_itertools.peekable[str]) -> types.Atom:
    peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

    if peek in '0123456789-+':
        str_value = ''.join(subr.itertools.takewhile_inclusive(lambda x: x in '0123456789-+.eE', input_stream))

        i, _ = subr.subr.trap(lambda: int(str_value))
        if i is not None:
            return types.Int(value=i)

        f, _ = subr.subr.trap(lambda: float(str_value))
        if f is not None:
            return types.Float(value=f)

        raise types.ReaderError(f'Could not parse as a number: {str_value}')

    if peek == '"':
        value = ''.join(subr.itertools.takewhile_inclusive(lambda x: x != '"', input_stream))
        return types.String(value=value)

    if peek == 't':
        subr.reader.ensure_char('true', input_stream)
        return types.Boolean(value=True)

    if peek == 'f':
        subr.reader.ensure_char('false', input_stream)
        return types.Boolean(value=False)

    if peek == 'n':
        subr.reader.ensure_char('null', input_stream)
        return types.Null()

    if peek == '[':
        subr.reader.ensure_char('[', input_stream)
        lst: list[types.Atom] = []
        while True:
            peek = subr.reader.peek_char(True, input_stream, recursive_p=True)
            if peek == ']':
                break
            lst.append(read_atom(input_stream))

        subr.reader.ensure_char(']', input_stream)
        return types.List(value=lst)

    if peek == '{':
        subr.reader.ensure_char('{', input_stream)
        obj = {}
        while True:
            peek = subr.reader.peek_char(True, input_stream, recursive_p=True)
            if peek == '}':
                break
            key = read_name(input_stream)
            subr.reader.ensure_char(':', input_stream)
            value = read_atom(input_stream)
            obj[key] = value

        subr.reader.ensure_char('}', input_stream)
        return types.Object(value=obj)

    return types.Enum(value=read_name(input_stream))



def read_operation_definition(input_stream: more_itertools.peekable[str]) -> types.OperationDefinition:
    type_pre = None
    variable_definitions: list[types.VariableDefinition] = []
    selection_set: list[Any] = []

    peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

    if peek == 'q':
        subr.reader.ensure_char('query', input_stream)
        type_pre = types.OperationTypeEnum.QUERY

    elif peek == 'm':
        subr.reader.ensure_char('mutation', input_stream)
        type_pre = types.OperationTypeEnum.MUTATION

    elif peek == 's':
        subr.reader.ensure_char('subscription', input_stream)
        type_pre = types.OperationTypeEnum.SUBSCRIPTION

    type_ = type_pre or types.OperationTypeEnum.QUERY

    name = read_name(input_stream, False)

    peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

    if peek == '(':
        next(input_stream)  # skip '('
        while True:
            subr.reader.ensure_char('$', input_stream)
            variable_name = read_name(input_stream)

            subr.reader.ensure_char(':', input_stream)

            type_ = read_type(input_stream)

            peek = subr.reader.peek_char(True, input_stream, recursive_p=True)

            if peek == '=':
                default = read_atom(input_stream)
            else:
                default = None

            if peek == '@':
                raise NotImplementedError  # Directives

            variable_definitions.append(types.VariableDefinition(
                name=variable_name,
                type_=type_,
                default=default,
                directives=[],
            ))

            peek = subr.reader.peek_char(True, input_stream, recursive_p=True)
            if peek == ')':
                break

    subr.reader.ensure_char('{', input_stream)
    while True:
        peek = subr.reader.peek_char(True, input_stream, recursive_p=True)
        if peek == '}':
            break




    return types.OperationDefinition(
        type_=types.OperationTypeEnum.QUERY,
        name=name,
        variable_definitions=variable_definitions,
        directives=[],
        selection_set=[]
    )


def read_definition(input_stream: more_itertools.peekable[str]) -> Optional[types.Definition]:
    return


def read_document(input_stream: more_itertools.peekable[str]) -> types.Document:
    lst: list[types.Definition] = []
    # while (res := read_definition(input_stream)) is not None:
    #     lst.append(res)

    lst.append(read_operation_definition(input_stream))

    return types.Document(value=lst)


def read(input_stream: more_itertools.peekable[str]) -> types.Document:
    # return read_document(input_stream)
    return read_type(input_stream)
