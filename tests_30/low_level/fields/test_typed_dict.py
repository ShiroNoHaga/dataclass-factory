from types import MappingProxyType
from typing import TypedDict

from dataclass_factory_30.low_level.fields import (
    TypedDictFieldsProvider,
    TypeFieldRequest,
    NoDefault,
    InputFieldsFigure,
    OutputFieldsFigure,
    GetterKind
)


class Foo(TypedDict, total=True):
    a: int
    b: str


class Bar(TypedDict, total=False):
    a: int
    b: str


TOTAL_FIELDS = [
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


def test_total_input():
    assert (
        TypedDictFieldsProvider()._get_input_fields_figure(Foo)
        ==
        InputFieldsFigure(
            extra=None,
            fields=TOTAL_FIELDS,
        )
    )


def test_total_output():
    assert (
        TypedDictFieldsProvider()._get_output_fields_figure(Foo)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ITEM,
            fields=TOTAL_FIELDS,
        )
    )


NON_TOTAL_FIELDS = [
    TypeFieldRequest(
        type=int,
        field_name='a',
        default=NoDefault(field_is_required=False),
        metadata=MappingProxyType({})
    ),
    TypeFieldRequest(
        type=str,
        field_name='b',
        default=NoDefault(field_is_required=False),
        metadata=MappingProxyType({})
    ),
]


def test_non_total_input():
    assert (
        TypedDictFieldsProvider()._get_input_fields_figure(Bar)
        ==
        InputFieldsFigure(
            extra=None,
            fields=NON_TOTAL_FIELDS,
        )
    )


def test_non_total_output():
    assert (
        TypedDictFieldsProvider()._get_output_fields_figure(Bar)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ITEM,
            fields=NON_TOTAL_FIELDS,
        )
    )