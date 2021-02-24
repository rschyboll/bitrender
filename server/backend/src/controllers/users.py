"""Module containing logic for users"""
import datetime
import bcrypt

from schema.user import UserCreate
from models.user import User
import storage.users as UserStorage

def __hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

async def register(user: UserCreate):
    """Register user in database"""
    password_hash = __hash_password(user.password)
    register_date = datetime.datetime.now()
    user_model = User(**user.dict(), password_hash = password_hash, register_date = register_date)
    UserStorage.create(user_model)
