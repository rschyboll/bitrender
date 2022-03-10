from fastapi import APIRouter

from bitrender.base.auth import hash_password
from bitrender.models import User
from bitrender.schemas.user import RegisterData

router = APIRouter(prefix="/users")


@router.post("/register")
async def register(user_data: RegisterData):
    """Registers a new user and assigns him the default role.

    Args:
        data (RegisterData): User data that is required in registration."""
    password_hash = hash_password(user_data.password)
    user = User(**user_data.dict(), password_hash=password_hash)
    await user.save()
