from fastapi import APIRouter, Depends, Response
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from bitrender.base.auth import (
    AclAction,
    AuthCheck,
    create_access_token,
    credentials_exception,
    hash_password,
)
from bitrender.models import User, UserAuth
from bitrender.schemas.user import UserLoginData, UserRegisterData

router = APIRouter(prefix="/users")


@atomic()
@router.post("/register")
async def register(data: UserRegisterData):
    """Registers a new user and assigns him the default role.

    Args:
        data (RegisterData): User data that is required in registration."""
    password_hash = hash_password(data.password.get_secret_value())
    user = User(email=data.email, username=data.username)
    await user.save()
    auth = UserAuth(password_hash=password_hash, user=user)
    await auth.save()


@atomic()
@router.post("/login")
async def login(response: Response, data: UserLoginData):
    #TODO change implementation to compatible with OAUTH
    user: User | None = None
    try:
        user = await User.get_by_username(data.login)
    except DoesNotExist:
        pass
    try:
        user = await User.get_by_email(data.login)
    except DoesNotExist:
        pass
    if user is None:
        raise credentials_exception
    access_token = create_access_token({"id": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)


async def create_user(data: UserRegisterData, auth_check: AuthCheck = Depends(AuthCheck)):
    async def create(data: UserRegisterData) -> User:
        pass

    await auth_check(create, AclAction.CREATE, [], (data,))
