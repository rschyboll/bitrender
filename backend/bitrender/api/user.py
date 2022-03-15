from fastapi import APIRouter
from tortoise.transactions import atomic

from bitrender.base.auth import hash_password
from bitrender.models import User, UserAuth
from bitrender.schemas.user import RegisterData

router = APIRouter(prefix="/users")


@atomic()
@router.post("/register")
async def register(user_data: RegisterData):
    """Registers a new user and assigns him the default role.

    Args:
        data (RegisterData): User data that is required in registration."""
    password_hash = hash_password(user_data.password)
    user = User(email=user_data.email)
    await user.save()
    auth = UserAuth(password_hash=password_hash, user=user)
    await auth.save()
