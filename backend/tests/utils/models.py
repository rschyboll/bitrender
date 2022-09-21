"""Contains models used only in testing."""
from __future__ import annotations

from typing import Literal, Type, TypeVar, Union, cast

from tortoise.fields import CharField, IntField
from tortoise.queryset import QuerySet

from bitrender.models.base import BaseModel
from bitrender.schemas.list_request import ListRequestInput

MODEL = TypeVar("MODEL", bound="ExampleModel")


class ExampleModel(BaseModel):
    """Database model used only for testing methods from BaseModel."""

    char_field = CharField(32)
    int_field = IntField()

    columns = Union[BaseModel.columns, Literal["char_field", "int_field"]]

    @classmethod
    def get_list(
        cls: Type[MODEL],
        request_input: ListRequestInput[ExampleModel.columns],
        lock: bool = True,
    ) -> QuerySet[MODEL]:
        return super(ExampleModel, cls).get_list(
            cast(ListRequestInput[BaseModel.columns], request_input), lock
        )
