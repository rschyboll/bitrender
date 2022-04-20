"""TODO generate docstring"""

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import TortoiseUserDatabase

from bitrender.models import User
from bitrender.schemas import UserAuth, UserCreate, UserSchema, UserUpdate

SECRET_KEY = "bb2a5daf96fd0cd95493b9a5f12ca4badadc5425663a0e391a2ed0f088b03026"


async def get_user_db():
    """TODO generate docstring"""

    yield TortoiseUserDatabase(UserAuth, User)


class UserManager(BaseUserManager[UserCreate, UserAuth]):
    """TODO generate docstring"""

    user_db_model = UserAuth
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY


async def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    """TODO generate docstring"""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """TODO generate docstring"""
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    UserSchema,
    UserCreate,
    UserUpdate,
    UserAuth,
)

current_active_user = fastapi_users.current_user(active=True)
