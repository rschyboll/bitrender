"""This module contains dependencies for user authorization."""
import asyncio
import inspect
from ctypes import Union
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Coroutine, Type, TypeVar, get_args, get_origin
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel as PydanticBase
from pydantic import ValidationError

from bitrender.models import User
from bitrender.models.base import BaseModel

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AclAction(Enum):
    """TODO generate docstring"""

    CREATE = "create"
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"


class AclPermit(Enum):
    """TODO generate docstring"""

    ALLOW = "Allow"
    DENY = "Deny"


AclEntry = tuple[AclPermit, list[str] | str, list[AclAction] | AclAction]

AclList = list[AclEntry]

EVERYONE = "system:everyone"
AUTHENTICATED = "system:authenticated"


class TokenData(PydanticBase):
    """Class containing decoded JWT data.

    Attributes:
        id (UUID) - User id"""

    id: UUID


def hash_password(password: str) -> bytes:
    """TODO generate docstring"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))


def check_password(password: str, password_hash: bytes) -> bool:
    """TODO generate docstring"""

    return bcrypt.checkpw(password.encode(), password_hash)


def create_access_token(data: dict) -> str:
    """TODO generate docstring"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """TODO generate docstring"""

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return TokenData(**payload)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """TODO generate docstring."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError) as error:
        raise credentials_exception from error
    user = await User.get_by_id(token_data.id, False)
    if user is None:
        raise credentials_exception
    return user


async def get_active_user(user: User = Depends(get_current_user)) -> User:
    """TODO generate docstring."""
    if user.active:
        return user
    raise credentials_exception


async def get_auth_ids(user: User = Depends(get_active_user)) -> list[str]:
    """TODO generate docstring."""
    return [*(await user.auth_ids), AUTHENTICATED]


ReturnT = TypeVar("ReturnT", bound=BaseModel)


class DBSelector:
    """TODO generate docstring."""

    def __init__(self, auth_ids: list[str] = Depends(get_auth_ids)):
        self.auth_ids = auth_ids

    async def __call__(
        self,
        selector: Callable[..., Coroutine[Any, Any, ReturnT]],
        actions: AclAction | list[AclAction],
        additional_model_types: list[Type[BaseModel]] = None,
        args: tuple = (),
    ) -> ReturnT:
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

    def __static_check(self, model_types: list[Type[BaseModel]], actions: list[AclAction]) -> bool:
        permits: list[AclPermit | None] = []
        for model_type in model_types:
            has_dacl = self.__has_dacl(model_type)
            acl_list = model_type.__sacl__()
            if acl_list is None and not has_dacl:
                raise credentials_exception
            elif acl_list is None:
                continue
            for action in actions:
                permit = self.__get_acllist_permit(acl_list, action)
                if permit is None and not has_dacl or permit == AclPermit.DENY:
                    raise credentials_exception
                permits.append(permit)
        return all(permit == AclPermit.ALLOW for permit in permits)

    async def __dynamic_check(self, model: ReturnT, actions: list[AclAction]):
        acl_lists = await model.__dacl__()
        if acl_lists is None:
            raise credentials_exception
        for acl_list in acl_lists:
            for action in actions:
                permit = self.__get_acllist_permit(acl_list, action)
                if permit is None or permit == AclPermit.DENY:
                    raise credentials_exception

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

    @classmethod
    def __has_dacl(cls, model_type: Type[BaseModel]) -> bool:
        signature = inspect.signature(model_type.__dacl__)
        return_type = signature.return_annotation
        if get_origin(return_type) is Union and None in get_args(return_type):
            return False
        return True


class TestModel(BaseModel):
    @classmethod
    def __sacl__(cls) -> list[AclEntry]:
        return [
            (AclPermit.ALLOW, "user:test", AclAction.VIEW),
            (AclPermit.DENY, "user:hello", AclAction.VIEW),
        ]

    async def __dacl__(self) -> list[list[AclEntry]]:
        return [
            [
                (AclPermit.ALLOW, "user:test23", AclAction.VIEW),
            ]
        ]


test = DBSelector(["user:test2"])


async def test_selector() -> TestModel:
    return TestModel()


asyncio.run(test(test_selector, AclAction.VIEW))
