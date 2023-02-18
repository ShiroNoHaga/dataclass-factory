import typing
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Tuple

import pytest

from adaptix._internal.feature_requirement import HAS_ANNOTATED
from adaptix._internal.model_tools import (
    AttrAccessor,
    DefaultFactory,
    DefaultValue,
    Figure,
    InputField,
    InputFigure,
    NoDefault,
    OutputField,
    OutputFigure,
    ParamKind,
    get_attrs_figure,
)
from adaptix._internal.model_tools.definitions import IntrospectionImpossible, ParamKwargs
from tests_helpers import requires

pytest.importorskip("attrs")

import attr
from attrs import define, field


@define
class NewStyle:
    a: int
    _b: str
    c: str = field(init=False)
    d: int = field(kw_only=True)

    e: int = 1
    f: int = field(default=2)
    g: list = field(factory=list)
    h: str = field(default='', metadata={'meta': 'data'})
    i: 'int' = field(default=3)


def test_new_style():
    assert (
        get_attrs_figure(NewStyle)
        ==
        Figure(
            input=InputFigure(
                constructor=NewStyle,
                kwargs=None,
                fields=(
                    InputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                    InputField(
                        type=str,
                        name='_b',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='b',
                    ),
                    InputField(
                        type=int,
                        name='e',
                        default=DefaultValue(1),
                        is_required=False,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='e',
                    ),
                    InputField(
                        type=int,
                        name='f',
                        default=DefaultValue(2),
                        is_required=False,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='f',
                    ),
                    InputField(
                        type=list,
                        name='g',
                        default=DefaultFactory(list),
                        is_required=False,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='g',
                    ),
                    InputField(
                        type=str,
                        name='h',
                        default=DefaultValue(''),
                        is_required=False,
                        metadata=MappingProxyType({'meta': 'data'}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='h',
                    ),
                    InputField(
                        type=int,
                        name='i',
                        default=DefaultValue(3),
                        is_required=False,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='i',
                    ),
                    InputField(
                        type=int,
                        name='d',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.KW_ONLY,
                        param_name='d',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=str,
                        name='_b',
                        default=NoDefault(),
                        accessor=AttrAccessor('_b', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=str,
                        name='c',
                        default=NoDefault(),
                        accessor=AttrAccessor('c', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='d',
                        default=NoDefault(),
                        accessor=AttrAccessor('d', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='e',
                        default=DefaultValue(1),
                        accessor=AttrAccessor('e', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='f',
                        default=DefaultValue(2),
                        accessor=AttrAccessor('f', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=list,
                        name='g',
                        default=DefaultFactory(list),
                        accessor=AttrAccessor('g', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=str,
                        name='h',
                        default=DefaultValue(''),
                        accessor=AttrAccessor('h', is_required=True),
                        metadata=MappingProxyType({'meta': 'data'}),
                    ),
                    OutputField(
                        type=int,
                        name='i',
                        default=DefaultValue(3),
                        accessor=AttrAccessor('i', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            ),
        )
    )


@attr.s
class OldStyle:
    a = attr.ib()
    b = attr.ib(type=int)
    c: int


def test_old_style():
    assert (
        get_attrs_figure(OldStyle)
        ==
        Figure(
            input=InputFigure(
                constructor=OldStyle,
                kwargs=None,
                fields=(
                    InputField(
                        type=Any,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                    InputField(
                        type=int,
                        name='b',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='b',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=Any,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='b',
                        default=NoDefault(),
                        accessor=AttrAccessor('b', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            ),
        )
    )


def int_factory():
    return 0


@define
class CustomInit:
    a: int
    b: int = field(factory=int_factory, metadata={'meta': 'data'})
    _c: int = field(kw_only=True)
    d: int = 10

    def __init__(self, a: str, b: str, c):
        self.__attrs_init__(int(a), int(b), int(c))


def test_custom_init():
    assert (
        get_attrs_figure(CustomInit)
        ==
        Figure(
            input=InputFigure(
                constructor=CustomInit,
                kwargs=None,
                fields=(
                    InputField(
                        type=str,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                    InputField(
                        type=str,
                        name='b',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({'meta': 'data'}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='b',
                    ),
                    InputField(
                        type=Any,
                        name='_c',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='c',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='b',
                        default=NoDefault(),
                        accessor=AttrAccessor('b', is_required=True),
                        metadata=MappingProxyType({'meta': 'data'}),
                    ),
                    OutputField(
                        type=int,
                        name='_c',
                        default=NoDefault(),
                        accessor=AttrAccessor('_c', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=int,
                        name='d',
                        default=NoDefault(),
                        accessor=AttrAccessor('d', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            )
        )
    )


@define
class CustomInitUnknownParams:
    a: int
    other: dict

    def __init__(self, a: int, b: str, c: bytes):
        self.__attrs_init__(a, {'b': b, 'c': c})


def test_custom_init_unknown_params():
    assert (
        get_attrs_figure(CustomInitUnknownParams)
        ==
        Figure(
            input=InputFigure(
                constructor=CustomInitUnknownParams,
                kwargs=None,
                fields=(
                    InputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                    InputField(
                        type=str,
                        name='b',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='b',
                    ),
                    InputField(
                        type=bytes,
                        name='c',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='c',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                    OutputField(
                        type=dict,
                        name='other',
                        default=NoDefault(),
                        accessor=AttrAccessor('other', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            )
        )
    )


@define
class CustomInitKwargs:
    a: int

    def __init__(self, a: int, **kwargs):
        self.__attrs_init__(a)


@define
class CustomInitKwargsTyped:
    a: int

    def __init__(self, a: int, **kwargs: str):
        self.__attrs_init__(a)


def test_custom_init_kwargs():
    assert (
        get_attrs_figure(CustomInitKwargs)
        ==
        Figure(
            input=InputFigure(
                constructor=CustomInitKwargs,
                kwargs=ParamKwargs(Any),
                fields=(
                    InputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            ),
        )
    )

    assert (
        get_attrs_figure(CustomInitKwargsTyped)
        ==
        Figure(
            input=InputFigure(
                constructor=CustomInitKwargsTyped,
                kwargs=ParamKwargs(str),
                fields=(
                    InputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=int,
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            ),
        )
    )


@define
class NoneAttr:
    a: None


def test_none_attr():
    assert (
        get_attrs_figure(NoneAttr)
        ==
        Figure(
            input=InputFigure(
                constructor=NoneAttr,
                kwargs=None,
                fields=(
                    InputField(
                        type=type(None),
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=type(None),
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            ),
        )
    )


@define
class NoneAttrCustomInit:
    a: None

    def __init__(self, a):
        self.__attrs_init__(a)


def test_none_attr_custom_init():
    assert (
        get_attrs_figure(NoneAttrCustomInit)
        ==
        Figure(
            input=InputFigure(
                constructor=NoneAttrCustomInit,
                kwargs=None,
                fields=(
                    InputField(
                        type=Any,
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=type(None),
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            )
        )
    )


@requires(HAS_ANNOTATED)
def test_annotated():
    @define
    class WithAnnotated:
        a: typing.Annotated[int, 'metadata']

    assert (
        get_attrs_figure(WithAnnotated)
        ==
        Figure(
            input=InputFigure(
                constructor=WithAnnotated,
                kwargs=None,
                fields=(
                    InputField(
                        type=typing.Annotated[int, 'metadata'],
                        name='a',
                        default=NoDefault(),
                        is_required=True,
                        metadata=MappingProxyType({}),
                        param_kind=ParamKind.POS_OR_KW,
                        param_name='a',
                    ),
                ),
            ),
            output=OutputFigure(
                fields=(
                    OutputField(
                        type=typing.Annotated[int, 'metadata'],
                        name='a',
                        default=NoDefault(),
                        accessor=AttrAccessor('a', is_required=True),
                        metadata=MappingProxyType({}),
                    ),
                ),
            )
        )
    )


def test_not_attrs():
    @dataclass
    class IAmDataclass:
        foo: int

    with pytest.raises(IntrospectionImpossible):
        get_attrs_figure(IAmDataclass)

    with pytest.raises(IntrospectionImpossible):
        get_attrs_figure(Tuple[IAmDataclass, int])

