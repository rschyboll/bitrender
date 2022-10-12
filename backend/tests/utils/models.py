"""Contains models used only in testing."""
from __future__ import annotations

from typing import Literal, TypeVar, Union

from tortoise.fields import CharField, IntField

from bitrender.models.base import BaseModel

MODEL = TypeVar("MODEL", bound="ExampleModel")


class ExampleModel(BaseModel):
    """Database model used only for testing methods from BaseModel."""

    char_field = CharField(32)
    int_field = IntField()

    columns = Union[BaseModel.columns, Literal["char_field", "int_field"]]
