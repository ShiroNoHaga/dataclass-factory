from collections import namedtuple
from types import MappingProxyType
from typing import Any, NamedTuple

from dataclass_factory_30.low_level.fields import (
    NamedTupleFieldsProvider,
    TypeFieldRequest,
    DefaultValue,
    NoDefault,
    InputFieldsFigure,
    OutputFieldsFigure,
    GetterKind
)

FooAB = namedtuple('FooAB', 'a b')
FooBA = namedtuple('FooBA', 'b a')


def test_order_ab():
    fields = [
        TypeFieldRequest(
            type=Any,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=Any,
            field_name='b',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        NamedTupleFieldsProvider()._get_input_fields_figure(FooAB)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        NamedTupleFieldsProvider()._get_output_fields_figure(FooAB)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )


def test_order_ba():
    fields = [
        TypeFieldRequest(
            type=Any,
            field_name='b',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=Any,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        NamedTupleFieldsProvider()._get_input_fields_figure(FooBA)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        NamedTupleFieldsProvider()._get_output_fields_figure(FooBA)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )


def func():
    return 0


FooDefs = namedtuple('FooDefs', 'a b c', defaults=[0, func])


def test_defaults():
    fields = [
        TypeFieldRequest(
            type=Any,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=Any,
            field_name='b',
            default=DefaultValue(0),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=Any,
            field_name='c',
            default=DefaultValue(func),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        NamedTupleFieldsProvider()._get_input_fields_figure(FooDefs)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        NamedTupleFieldsProvider()._get_output_fields_figure(FooDefs)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )


BarA = NamedTuple('BarA', a=int, b=str)

# ClassVar do not supported in NamedTuple


class BarB(NamedTuple):
    a: int
    b: str = 'abc'


def test_class_hinted_namedtuple():
    fields = [
        TypeFieldRequest(
            type=int,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=str,
            field_name='b',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        NamedTupleFieldsProvider()._get_input_fields_figure(BarA)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        NamedTupleFieldsProvider()._get_output_fields_figure(BarA)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )


def test_hinted_namedtuple():
    fields = [
        TypeFieldRequest(
            type=int,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=str,
            field_name='b',
            default=DefaultValue('abc'),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        NamedTupleFieldsProvider()._get_input_fields_figure(BarB)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        NamedTupleFieldsProvider()._get_output_fields_figure(BarB)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )