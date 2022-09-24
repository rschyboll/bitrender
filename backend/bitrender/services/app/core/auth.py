import inspect
from typing import Any, Callable, Coroutine, Type, TypeVar, get_args, overload

from antidote import implements, inject, wire
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic

from bitrender.core.acl import AclAction, AclResource
from bitrender.errors.user import UnauthorizedError
from bitrender.models.base import BaseModel
from bitrender.services.app.core import BaseAppService
from bitrender.services.app.interfaces.auth import IAuthService
from bitrender.services.helpers import IACLHelper

MODEL = TypeVar("MODEL", bound=BaseModel)
RESOURCE = TypeVar("RESOURCE", bound=AclResource | list[AclResource])


@wire
@implements(IAuthService)
class AuthService(BaseAppService, IAuthService):
    """TODO generate docstring"""

    def __init__(self, acl_helper: IACLHelper = inject.me()):
        BaseAppService.__init__(self)
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
        if additional_types is None:
            additional_types = []
        auth_ids = self.context.auth_ids
        return_type = self.__get_query_return_type(query)
        if return_type is None:
            raise UnauthorizedError()
        types = [*additional_types, return_type]
        static_check_result = self.__acl_helper.static(types, AclAction.VIEW, auth_ids)
        if static_check_result:
            query_result: list[MODEL] | MODEL = await query
            return query_result
        if static_check_result is None:
            query_result = await query
            dynamic_result = await self.__acl_helper.dynamic(query_result, AclAction.VIEW, auth_ids)
            if dynamic_result:
                return query_result
        raise UnauthorizedError()

    @staticmethod
    def __get_query_return_type(
        query: QuerySet[MODEL] | QuerySetSingle[MODEL],
    ) -> Type[BaseModel] | None:
        if isinstance(query, QuerySet):
            query_type = query.model
            if issubclass(query_type, BaseModel):
                return query_type
        return None

    @atomic()
    async def action(
        self,
        action: Callable[..., Coroutine[Any, Any, RESOURCE]],
        acl_actions: AclAction | list[AclAction],
        args: list[Any] | dict[Any, Any] | None = None,
        additional_static_resources: list[Type[AclResource]] | None = None,
    ) -> RESOURCE:
        if args is None:
            args = []
        auth_ids = self.context.auth_ids
        static_types = self.__get_action_return_type(action, additional_static_resources)
        static_result = self.__acl_helper.static(static_types, acl_actions, auth_ids)
        if static_result:
            return await (action(*args) if isinstance(args, list) else action(**args))
        if static_result is None:
            action_result = await (action(*args) if isinstance(args, list) else action(**args))
            dynamic_result = await self.__acl_helper.dynamic(action_result, acl_actions, auth_ids)
            if dynamic_result:
                return action_result
        raise UnauthorizedError()

    @staticmethod
    def __get_action_return_type(
        action: Callable[..., Coroutine[Any, Any, RESOURCE]], types: list[Type[AclResource]] | None
    ) -> list[Type[AclResource]]:
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
