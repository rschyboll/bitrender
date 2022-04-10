from fastapi import APIRouter, Depends
from tortoise.transactions import atomic

from bitrender.base.auth import AclAction, AuthCheck, hash_password
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
async def login(data: UserLoginData):
    pass


async def create_user(data: UserRegisterData, auth_check: AuthCheck = Depends(AuthCheck)):
    async def create(data: UserRegisterData) -> User:
        pass

    await auth_check(create, AclAction.CREATE, [], (data,))
