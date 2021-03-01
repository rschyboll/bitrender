"""Module containing logic for users"""
import datetime
import bcrypt

from schema.user import UserCreate
from storage import users as UserStorage, NotFoundException

def __hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

async def authenticate_user(login: str, password: str) -> bool:
    try:
        user = await UserStorage.get_by_login(login)
    except NotFoundException:
        return False
    hashed_password = __hash_password(password)
    if user.password_hash == hashed_password:
        return True

async def register(user: UserCreate):
    """Register user in database"""
    password_hash = __hash_password(user.password)
    register_date = datetime.datetime.now()
    await UserStorage.create(user, password_hash, register_date)
