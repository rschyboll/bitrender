"""TODO generate docstring"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import BaseORMException, DoesNotExist
from tortoise.transactions import atomic

from bitrender.base.auth import create_access_token, credentials_exception, hash_password
from bitrender.models import User, UserAuth
from bitrender.models.role import Role
from bitrender.schemas.user import UserRegisterData

router = APIRouter(prefix="/users")


async def __get_default_role() -> Role:
    try:
        return await Role.get_default(False)
    except DoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from error


@atomic()
async def __register_user(password_hash: bytes, data: UserRegisterData, role: Role) -> User:
    try:
        user = User(email=data.email, username=data.username, role=role)
        await user.save()
        user_auth = UserAuth(password_hash=password_hash, user=user)
        await user_auth.save()
        return user
    except BaseORMException as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from error


@router.post("/register")
async def register(data: UserRegisterData):
    """Registers a new user and assigns him the default role.

    Args:
        data (RegisterData): User data that is required in registration."""
    password_hash = hash_password(data.password.get_secret_value())
    default_role = await __get_default_role()
    await __register_user(password_hash, data, default_role)


@atomic()
@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    """TODO change implementation to compatible with OAUTH"""
    try:
        user = await User.get_by_username(data.username)
        if not user.active:
            raise credentials_exception
    except DoesNotExist as error:
        raise credentials_exception from error
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
