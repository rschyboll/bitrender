"""TODO generate docstring"""
from __future__ import annotations

import inspect
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    get_args,
    overload,
)
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import EmailStr
from tortoise.exceptions import DoesNotExist
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic

from bitrender.auth.acl import AclAction
from bitrender.auth.jwt import TokenData
from bitrender.errors.auth import (
    AlreadyVerified,
    BadCredentials,
    CredentialsError,
    NoDefaultRole,
    UserNotVerified,
    VerificationFailed,
)
from bitrender.errors.user import UserDoesNotExist
from bitrender.models import Role, User
from bitrender.models.base import BaseModel
from bitrender.schemas.user import UserCreate

if TYPE_CHECKING:
    from bitrender.services import Services


class PasswordHelperProtocol(Protocol):
    """TODO generate docstring"""

    def hash(self, password: str) -> bytes:
        """TODO generate docstring"""

    def verify(self, password: str, hashed_password: bytes) -> bool:
        """TODO generate docstring"""


class TokenHelperProtocol(Protocol):
    """TODO generate docstring"""

    def create_token(self, user_id: UUID) -> str:
        """TODO generate docstring"""

    def decode_token(self, token: str) -> TokenData:
        """TODO generate docstring"""


class AclHelperProtocol(Protocol):
    """TODO generate docstring"""

    def static_check(
        self, models: Sequence[Type[BaseModel]], actions: AclAction | Sequence[AclAction]
    ) -> bool | None:
        """TODO generate docstring"""

    async def dynamic_check(
        self, models: BaseModel | Sequence[BaseModel], actions: AclAction | Sequence[AclAction]
    ) -> bool | None:
        """TODO generate docstring"""


MODEL = TypeVar("MODEL", bound=BaseModel)
RETURNT = TypeVar("RETURNT", bound=BaseModel | list[BaseModel])


class AuthService:
    """TODO generate docstring"""

    def __init__(
        self,
        services: Services,
        password_helper: PasswordHelperProtocol,
        token_helper: TokenHelperProtocol,
        acl_helper: AclHelperProtocol,
    ):
        self.services = services
        self.password = password_helper
        self.token = token_helper
        self.acl = acl_helper

    async def register(self, user_data: UserCreate) -> User:
        """TODO generate docstring"""
        try:
            role = await Role.get_default(False)
        except DoesNotExist as error:
            raise NoDefaultRole() from error
        return await self.services.user.create(user_data, role)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> str:
        """TODO generate docstring"""
        try:
            user = await User.get_by_email(credentials.username)
        except DoesNotExist as error:
            raise BadCredentials() from error
        if not self.password.verify(credentials.password, user.hashed_password):
            raise BadCredentials()
        if not user.is_verified:
            raise UserNotVerified()
        if not user.is_active:
            raise BadCredentials()
        return self.token.create_token(user.id)

    async def request_verify(self, email: EmailStr) -> None:
        """TODO generate docstring"""
        try:
            user = await User.get_by_email(email)
        except DoesNotExist as error:
            raise UserDoesNotExist() from error
        token = self.token.create_token(user.id)
        if user.is_verified:
            raise AlreadyVerified()
        user.verify_token = token
        await user.save()
        await self.services.email.send_verify_email(user.email, token)

    async def verify(self, email: EmailStr, token: str) -> None:
        """TODO generate docstring"""
        try:
            user = await User.get_by_email(email)
        except DoesNotExist as error:
            raise UserDoesNotExist() from error
        try:
            token_data = self.token.decode_token(token)
            if token != user.verify_token or token_data.sub != user.id:
                raise VerificationFailed()
            user.is_verified = True
            await user.save()
        except JWTError as error:
            raise VerificationFailed() from error

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
        static_types = self.__get_query_static_types(query, additional_static_models)
        static_result = self.acl.static_check(static_types, AclAction.VIEW)
        if static_result:
            return await query
        if static_result is None:
            query_result = await query
            dynamic_result = await self.acl.dynamic_check(query_result, AclAction.VIEW)
            if dynamic_result:
                return query_result
        raise CredentialsError()

    @staticmethod
    def __get_query_static_types(
        query: QuerySet | QuerySetSingle, types: list[Type[BaseModel]] | None
    ) -> list[Type[BaseModel]]:
        if types is None:
            types = []
        if isinstance(query, QuerySet):
            query_type = query.model
            if isinstance(query_type, BaseModel):
                return [*types, query_type]
        raise CredentialsError()

    @atomic()
    async def action(
        self,
        action: Callable[..., Coroutine[Any, Any, RETURNT]],
        acl_actions: AclAction | list[AclAction],
        args: tuple | dict = (),
        additional_static_models: list[Type[BaseModel]] = None,
    ) -> RETURNT:
        """TODO generate docstring"""
        static_types = self.__get_action_static_types(action, additional_static_models)
        static_result = self.acl.static_check(static_types, acl_actions)
        if static_result:
            return await (action(*args) if isinstance(args, tuple) else action(**args))
        if static_result is None:
            action_result = await (action(*args) if isinstance(args, tuple) else action(**args))
            dynamic_result = await self.acl.dynamic_check(action_result, acl_actions)
            if dynamic_result:
                return action_result
        raise CredentialsError()

    @staticmethod
    def __get_action_static_types(
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
