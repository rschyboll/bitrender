# pylint: disable=unused-import
# pylint: disable=invalid-name
from datetime import datetime
from typing import Any, Generic, List, Literal, Optional, Type, TypeVar, Union, overload
from uuid import UUID

from tortoise.fields import DatetimeField, UUIDField
from tortoise.models import Model

from schemas.base import BaseView

_VIEW = TypeVar("_VIEW", bound="BaseView")
_MODEL = TypeVar("_MODEL", bound="BaseModel[_VIEW]")  # type: ignore


class BaseModel(Model, Generic[_VIEW]):
    id: UUID = UUIDField(pk=True)
    create_date: datetime = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def to_view(self) -> _VIEW:
        raise NotImplementedError()

    @overload
    @classmethod
    async def get_all(cls: Type[_MODEL], view: Literal[False] = ...) -> List[_MODEL]:
        ...

    @overload
    @classmethod
    async def get_all(cls: Type[_MODEL], view: Literal[True]) -> List[_VIEW]:
        ...

    @classmethod
    async def get_all(
        cls: Type[_MODEL], view: bool = False
    ) -> Union[List[_MODEL], List[_VIEW]]:
        if not view:
            return await cls.all().select_for_update()
        return [model.to_view() for model in await cls.all()]

    @overload
    @classmethod
    async def get_by_id(
        cls: Type[_MODEL], model_id: UUID, view: Literal[False] = ...
    ) -> _MODEL:
        ...

    @overload
    @classmethod
    async def get_by_id(
        cls: Type[_MODEL], model_id: UUID, view: Literal[True]
    ) -> _VIEW:
        ...

    @classmethod
    async def get_by_id(
        cls: Type[_MODEL], model_id: UUID, view: bool = False
    ) -> Union[_MODEL, _VIEW]:
        if not view:
            return await cls.select_for_update().get(id=model_id)
        return (await cls.all().get(id=model_id)).to_view()

    @overload
    @classmethod
    async def get_latest(
        cls: Type[_MODEL], view: Literal[False] = ...
    ) -> Optional[_MODEL]:
        ...

    @overload
    @classmethod
    async def get_latest(cls: Type[_MODEL], view: Literal[True]) -> Optional[_VIEW]:
        ...

    @classmethod
    async def get_latest(
        cls: Type[_MODEL], view: bool = False
    ) -> Union[Optional[_MODEL], Optional[_VIEW]]:
        if not view:
            return await cls.select_for_update().order_by("-create_date").first()
        model = await cls.all().order_by("-create_date").first()
        if model is None:
            return None
        return model.to_view()
