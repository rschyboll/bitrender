from datetime import datetime

from models.user import User
from schema.user import UserCreate, UserView
from tortoise.transactions import atomic


async def create(user_data: UserCreate, password_hash: bytes, register_date: datetime) -> UserView:
    user: User = User(**user_data.dict(), password_hash = password_hash, register_date = register_date)
    await user.save()
    return UserView.from_orm(user)

async def get(user_id: int) -> UserView:
    user: User = await User.get(id=user_id)
    return UserView.from_orm(user)

async def get_by_login(user_login: str) -> UserView:
    user: User = await User.get(login=user_login)
    return UserView.from_orm(user)

async def get_user_password_hash(user_login: str) -> bytes:
    user: User = await User.get(login=user_login)
    return user.password_hash
