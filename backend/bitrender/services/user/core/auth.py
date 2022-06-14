import inspect
from typing import Any, Callable, Coroutine, Type, TypeVar, get_args, overload

from antidote import implements, inject, wire
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic

from bitrender.core.acl import AclAction
from bitrender.errors.auth import CredentialsError
from bitrender.models.base import BaseModel
from bitrender.services.user import IUserServices
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.auth import IAuthService
from bitrender.services.utils import IACLHelper

MODEL = TypeVar("MODEL", bound=BaseModel)
RETURNT = TypeVar("RETURNT", bound=BaseModel | list[BaseModel])


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

    async def query(
        self,
        query: QuerySet[MODEL] | QuerySetSingle[MODEL],
        additional_types: list[Type[BaseModel]] | None = None,
    ) -> list[MODEL] | MODEL:
        return_type = self.__get_query_return_type(query)
        types = [*additional_types, return_type]
        static_check_result = self.__acl_helper.static(types, AclAction.VIEW)
        if static_check_result:
            return await query
        if static_check_result is None:
            query_result = await query
            dynamic_result = await self.__acl_helper.dynamic(query_result, AclAction.VIEW)
            if dynamic_result:
                return query_result
        raise CredentialsError()

    @staticmethod
    def __get_query_return_type(query: QuerySet | QuerySetSingle) -> Type[BaseModel] | None:
        if isinstance(query, QuerySet):
            query_type = query.model
            if issubclass(query_type, BaseModel):
                return query_type
        return None

    @atomic()
    async def action(
        self,
        action: Callable[..., Coroutine[Any, Any, RETURNT]],
        acl_actions: AclAction | list[AclAction],
        args: tuple | dict = (),
        additional_static_models: list[Type[BaseModel]] = None,
    ) -> RETURNT:
        """TODO generate docstring"""
        static_types = self.__get_action_return_type(action, additional_static_models)
        static_result = self.__acl_helper.static(static_types, acl_actions)
        if static_result:
            return await (action(*args) if isinstance(args, tuple) else action(**args))
        if static_result is None:
            action_result = await (action(*args) if isinstance(args, tuple) else action(**args))
            dynamic_result = await self.__acl_helper.dynamic(action_result, acl_actions)
            if dynamic_result:
                return action_result
        raise CredentialsError()

    @staticmethod
    def __get_action_return_type(
        action: Callable, types: list[Type[BaseModel]] | None
    ) -> list[Type[BaseModel]]:
        if types is None:
            types = []
        signature = inspect.signature(action)
        return_type = signature.return_annotation
        try:
            if issubclass(return_type, BaseModel):
                return [*types, return_type]
        except TypeError:
            pass
        try:
            if isinstance(return_type, TypeVar):
                if issubclass(action.__self__, BaseModel):  # type: ignore
                    return [*types, action.__self__]  # type: ignore
        except TypeError:
            pass
        if isinstance(return_type, list):
            return_type = get_args(return_type)[0]
            if issubclass(return_type, BaseModel):
                return [*types, return_type]
        raise Exception("Action has wrong return type")
