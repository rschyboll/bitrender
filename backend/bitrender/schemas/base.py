"""This module contains the base class for all pydantic schemas."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as BaseSchema

from bitrender.models import BaseModel  # pylint: disable=unused-import

_MODEL = TypeVar("_MODEL", bound="BaseModel")


class BaseView(BaseSchema, ABC, Generic[_MODEL]):
    """Class that serves as the base for all pydantic schemas.

    Attributes:
        id (UUID): Primary key of the database entry.
        created_at (datetime): Datetime, when the entry was created.
        modified_at (datetime): Datetime, when the entry was last modified."""

    id: UUID
    created_at: datetime
    modified_at: datetime

    @abstractmethod
    def to_model(self) -> _MODEL:
        """Converts the schema to it's corresponding database model.
        Does not save the model to the database."""

    class Config:
        """BaseView config."""

        orm_mode = True
