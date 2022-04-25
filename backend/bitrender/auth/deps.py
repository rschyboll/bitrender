import inspect
from typing import Any, Callable, Coroutine, Type, TypeVar, get_args

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction

from bitrender.auth.acl import (
    AUTHENTICATED,
    EVERYONE,
    SUPERUSER,
    AclAction,
    AclEntry,
    AclList,
    AclPermit,
)
from bitrender.auth.jwt import decode_token, jwt
from bitrender.models import Permission, User
from bitrender.models.base import BaseModel


class CredentialsException(HTTPException):
    """TODO generate costring"""

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Not authenticated",
        headers: dict[str, Any] | None = None,
    ) -> None:
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class OAuth2PasswordBearerWithCookie(OAuth2):
    """TODO generate docstring"""

    def __init__(self, tokenUrl: str, auto_error: bool = True):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")
        if authorization is None:
            raise CredentialsException()

        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise CredentialsException()
            return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie("/login", False)


async def get_current_user_or_none(token: str | None = Depends(oauth2_scheme)) -> User | None:
    """Extracts user data from the JWT, validates it and returns the current user.
    Returns None, if the token is expired, is corrupted, or when the user does not exist.

    Args:
        token (str | None, optional): JWT token extracted from Request headers.\
            Defaults to Depends(oauth2_scheme).

    Returns:
        User | None: Current user, or None, if no user could be authenticated."""
    if token is None:
        return None
    try:
        token_data = decode_token(token)
        user = await User.get_by_id(token_data.sub, False)
        return user
    except (jwt.JWTError, ValidationError, DoesNotExist):
        return None


async def get_auth_ids(user: User | None = Depends(get_current_user_or_none)) -> list[str]:
    """TODO generate docstring."""
    if user is None or not user.is_active or not user.is_verified:
        return [EVERYONE]
    if user.is_superuser:
        return [*(await user.acl_id_list), SUPERUSER, AUTHENTICATED, EVERYONE]
    return [*(await user.acl_id_list), AUTHENTICATED, EVERYONE]


ReturnT = TypeVar("ReturnT", bound=BaseModel)


class AuthCheck:
    """TODO generate docstring."""

    def __init__(self, auth_ids: list[str] = Depends(get_auth_ids)):
        self.auth_ids = auth_ids

    async def __call__(
        self,
        selector: Callable[..., Coroutine[Any, Any, ReturnT]],
        actions: AclAction | list[AclAction],
        args: tuple = (),
        additional_model_types: list[Type[BaseModel]] = None,
    ) -> ReturnT:
        async with in_transaction():
            if additional_model_types is None:
                additional_model_types = []
            if not isinstance(actions, list):
                actions = [actions]
            return_type = self.__get_selector_returntype(selector)
            static_check = self.__static_check([*additional_model_types, return_type], actions)
            model = await selector(*args)
            if static_check:
                return model
            await self.__dynamic_check(model, actions)
            return model

    async def has_permission(self, permission: Permission):
        """TODO generate docstring"""
        return permission.acl_id in self.auth_ids

    def __static_check(self, model_types: list[Type[BaseModel]], actions: list[AclAction]) -> bool:
        permits: list[AclPermit | None] = []
        for model_type in model_types:
            acl_list = model_type.__sacl__()
            if acl_list is None:
                continue
            for action in actions:
                permit = self.__get_acllist_permit(acl_list, action)
                if permit == AclPermit.DENY:
                    raise CredentialsException()
                permits.append(permit)
        return all(permit == AclPermit.ALLOW for permit in permits)

    async def __dynamic_check(self, model: ReturnT, actions: list[AclAction]):
        acl_lists = await model.__dacl__()
        if acl_lists is None:
            raise CredentialsException()
        for acl_list in acl_lists:
            for action in actions:
                permit = self.__get_acllist_permit(acl_list, action)
                if permit is None or permit == AclPermit.DENY:
                    raise CredentialsException()

    def __get_acllist_permit(
        self, acl_list: AclList, required_action: AclAction
    ) -> AclPermit | None:
        for entry in acl_list:
            permit = self.__get_acl_permit(entry, required_action)
            if permit is not None:
                return permit
        return None

    def __get_acl_permit(self, entry: AclEntry, required_action: AclAction) -> AclPermit | None:
        permit = entry[0]
        auth_ids = entry[1]
        actions = entry[2]
        if not isinstance(auth_ids, list):
            auth_ids = [auth_ids]
        if not isinstance(actions, list):
            actions = [actions]
        if permit == AclPermit.NOTALLOW:
            if required_action in actions and all(
                auth_id not in self.auth_ids for auth_id in auth_ids
            ):
                return AclPermit.ALLOW
        if permit == AclPermit.NOTDENY:
            if required_action in actions and all(
                auth_id not in self.auth_ids for auth_id in auth_ids
            ):
                return AclPermit.DENY
        if required_action in actions and all(auth_id in self.auth_ids for auth_id in auth_ids):
            return permit
        return None

    @classmethod
    def __get_selector_returntype(cls, selector: Callable) -> Type[BaseModel]:
        signature = inspect.signature(selector)
        return_type = signature.return_annotation
        if isinstance(return_type, list):
            return get_args(return_type)[0]
        return return_type
