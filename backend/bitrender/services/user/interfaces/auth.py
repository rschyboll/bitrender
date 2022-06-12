from typing import Type, TypeVar, overload

from antidote import interface
from tortoise.queryset import QuerySet, QuerySetSingle

from bitrender.models.base import BaseModel

from . import IService

MODEL = TypeVar("MODEL", bound=BaseModel)


@interface
class IAuthService(IService):
    """Service used for authorizing user access."""

    @overload
    async def query(
        self,
        query: QuerySet[MODEL],
        additional_static_models: list[Type[BaseModel]] | None = ...,
    ) -> list[MODEL]:
        ...

    @overload
    async def query(
        self,
        query: QuerySetSingle[MODEL],
        additional_static_models: list[Type[BaseModel]] | None = ...,
    ) -> MODEL:
        ...

    async def query(
        self,
        query: QuerySet[MODEL] | QuerySetSingle[MODEL],
        additional_static_models: list[Type[BaseModel]] | None = None,
    ) -> list[MODEL] | MODEL:
        """TODO generate docstring"""
