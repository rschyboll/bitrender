"""TODO generate docstring"""
from abc import abstractmethod
from typing import Any, Callable, Coroutine, Type, TypeVar, overload

from antidote import interface
from tortoise.queryset import QuerySet, QuerySetSingle

from bitrender.core.acl import AclAction
from bitrender.models.base import BaseModel

from . import IService

MODEL = TypeVar("MODEL", bound=BaseModel)
RETURNT = TypeVar("RETURNT", bound=BaseModel | list[BaseModel])


@interface
class IAuthService(IService):
    """Service used for authorizing user access to resources."""

    @overload
    async def query(
        self,
        query: QuerySet[MODEL],
        additional_types: list[Type[BaseModel]] | None = ...,
    ) -> list[MODEL]:
        ...

    @overload
    async def query(
        self,
        query: QuerySetSingle[MODEL],
        additional_types: list[Type[BaseModel]] | None = ...,
    ) -> MODEL:
        ...

    @abstractmethod
    async def query(
        self,
        query: QuerySet[MODEL] | QuerySetSingle[MODEL],
        additional_types: list[Type[BaseModel]] | None = None,
    ) -> list[MODEL] | MODEL:
        """TODO generate docstring"""

    @abstractmethod
    async def action(
        self,
        action: Callable[..., Coroutine[Any, Any, RETURNT]],
        acl_actions: AclAction | list[AclAction],
        args: list[Any] | dict[Any, Any] | None = None,
        additional_static_models: list[Type[BaseModel]] | None = None,
    ) -> RETURNT:
        """TODO generate docstring"""
