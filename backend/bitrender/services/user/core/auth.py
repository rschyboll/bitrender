from typing import Type, TypeVar, overload
from uuid import UUID

from antidote import implements, inject, wire
from tortoise.queryset import QuerySet, QuerySetSingle

from bitrender.models.base import BaseModel
from bitrender.services.user import IUserServices
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.auth import IAuthService
from bitrender.services.utils import IACLHelper

MODEL = TypeVar("MODEL", bound=BaseModel)


@wire
@implements(IAuthService).by_default
class AuthService(Service, IAuthService):
    """TODO generate docstring"""

    def __init__(self, services: IUserServices | None = None, acl_helper: IACLHelper = inject.me()):
        Service.__init__(self, services)
        self.__acl_helper = acl_helper

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
        pass
