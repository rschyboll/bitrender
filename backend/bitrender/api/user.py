"""TODO generate docstring"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import BaseORMException, DoesNotExist
from tortoise.transactions import atomic

from bitrender.auth.password import BCryptHelper
from bitrender.models import User, UserAuth
from bitrender.models.role import Role
from bitrender.schemas.user import UserRegister, UserSchema

router = APIRouter(prefix="/users")


async def __get_default_role() -> Role:
    try:
        return await Role.get_default(False)
    except DoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from error


@atomic()
@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED, responses={}
)
async def register(data: UserRegister):
    """Registers a new user and assigns him the default role.

    Args:
        data (RegisterData): User data that is required in registration."""
    hashed_password = BCryptHelper.hash(data.password)
    default_role = await __get_default_role()
    await __register_user(hashed_password, data, default_role)


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
