"""CRUD utilities for user"""
from datetime import datetime
from tortoise.transactions import atomic

from models.user import User
from schema.user import UserCreate, UserView

@atomic()
async def create(user_data: UserCreate, password_hash: bytes, register_date: datetime) -> UserView:
    user: User = User(**user_data.dict(), password_hash = password_hash, register_date = register_date)
    await user.save()
    return UserView.from_orm(user)

@atomic()
async def get(user_id: int) -> UserView:
    user: User = await User.get(id=user_id)
    return UserView.from_orm(user)

@atomic()
async def get_by_login(user_login: str) -> UserView:
    user: User = await User.get(login=user_login)
    return UserView.from_orm(user)
