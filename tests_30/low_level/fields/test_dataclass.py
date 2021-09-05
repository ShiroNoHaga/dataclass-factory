from dataclasses import dataclass, field
from types import MappingProxyType
from typing import ClassVar

from dataclass_factory_30.low_level.fields import (
    DataclassFieldsProvider,
    TypeFieldRequest,
    NoDefault,
    DefaultValue,
    DefaultFactory,
    InputFieldsFigure,
    OutputFieldsFigure,
    GetterKind
)


@dataclass
class Foo:
    a: int
    b: str = 'text'
    c: list = field(default_factory=list)
    d: int = field(default=3, init=False)
    e: ClassVar[int]
    f: ClassVar[int] = 1
    g: int = field(default=4, metadata={'meta': 'data'})


def test_input():
    assert (
        DataclassFieldsProvider()._get_input_fields_figure(Foo)
        ==
        InputFieldsFigure(
            extra=None,
            fields=[
                TypeFieldRequest(
                    type=int,
                    field_name='a',
                    default=NoDefault(field_is_required=True),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=str,
                    field_name='b',
                    default=DefaultValue('text'),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=list,
                    field_name='c',
                    default=DefaultFactory(list),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=int,
                    field_name='g',
                    default=DefaultValue(4),
                    metadata=MappingProxyType({'meta': 'data'})
                ),
            ],
        )
    )


def test_output():
    assert (
        DataclassFieldsProvider()._get_output_fields_figure(Foo)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=[
                TypeFieldRequest(
                    type=int,
                    field_name='a',
                    default=NoDefault(field_is_required=True),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=str,
                    field_name='b',
                    default=DefaultValue('text'),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=list,
                    field_name='c',
                    default=DefaultFactory(list),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=int,
                    field_name='d',
                    default=DefaultValue(3),
                    metadata=MappingProxyType({})
                ),
                TypeFieldRequest(
                    type=int,
                    field_name='g',
                    default=DefaultValue(4),
                    metadata=MappingProxyType({'meta': 'data'})
                ),
            ],
        )
    )


@dataclass
class Bar:
    a: int


@dataclass
class ChildBar(Bar):
    b: int


def test_inheritance():
    fields = [
        TypeFieldRequest(
            type=int,
            field_name='a',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
        TypeFieldRequest(
            type=int,
            field_name='b',
            default=NoDefault(field_is_required=True),
            metadata=MappingProxyType({})
        ),
    ]

    assert (
        DataclassFieldsProvider()._get_input_fields_figure(ChildBar)
        ==
        InputFieldsFigure(
            extra=None,
            fields=fields,
        )
    )

    assert (
        DataclassFieldsProvider()._get_output_fields_figure(ChildBar)
        ==
        OutputFieldsFigure(
            getter_kind=GetterKind.ATTR,
            fields=fields,
        )
    )