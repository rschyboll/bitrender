"""This module contains the base class for all database models."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, List, Literal, Type, TypeVar, Union, overload
from uuid import UUID

from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model

from bitrender.schemas.base import BaseView  # pylint: disable=unused-import

_VIEW = TypeVar("_VIEW", bound="BaseView")
_MODEL = TypeVar("_MODEL", bound="BaseModel[_VIEW]")  # type: ignore


class BaseModel(Model, ABC, Generic[_VIEW]):
    """Class that serves as the base for all database models.

    Attributes:
        id (UUID): Primary key of the database entry.
        create_time (datetime): Datetime, when the entry was created."""

    id: UUID = UUIDField(pk=True)
    created_at: datetime = DatetimeField(auto_now_add=True)

    class Meta:
        """BaseModel config."""

        abstract = True

    @abstractmethod
    def to_view(self) -> _VIEW:
        """Converts the model to it's corresponding pydantic schema."""

    @overload
    @classmethod
    async def get_all(cls: Type[_MODEL], view: Literal[False] = ...) -> List[_MODEL]:
        ...

    @overload
    @classmethod
    async def get_all(cls: Type[_MODEL], view: Literal[True]) -> List[_VIEW]:
        ...

    @classmethod
    async def get_all(cls: Type[_MODEL], view: bool = False) -> Union[List[_MODEL], List[_VIEW]]:
        """Returns all database entries of the given model.

        Args:
            view (bool, optional): Specifies if the models should be converted to schemas.
                Defaults to False.

        Returns:
            List[_MODEL]: If view is False. A list with instances of the model.
                Locks the rows in the database.
            List[_VIEW]: If view if True. A list with schemas created from the model.
                Does not lock the rows in the database."""
        if not view:
            return await cls.all().select_for_update()
        return [model.to_view() for model in await cls.all()]

    @overload
    @classmethod
    async def get_by_id(cls: Type[_MODEL], model_id: UUID, view: Literal[False] = ...) -> _MODEL:
        ...

    @overload
    @classmethod
    async def get_by_id(cls: Type[_MODEL], model_id: UUID, view: Literal[True]) -> _VIEW:
        ...

    @classmethod
    async def get_by_id(
        cls: Type[_MODEL], model_id: UUID, view: bool = False
    ) -> Union[_MODEL, _VIEW]:
        """Returns a database entry based provided id.

        Args:
            model_id (UUID): Id of the database entry that should be returned.
            view (bool, optional): Specifies if the model should be converted to it's schema.
                Defaults to False.

        Returns:
            _MODEL: If view is False. Instances of the model.
                Locks the row in the database.
            _VIEW: If view if True. Schema created from the model.
                Does not lock the row in the database."""
        if not view:
            return await cls.select_for_update().get(id=model_id)
        return (await cls.all().get(id=model_id)).to_view()
