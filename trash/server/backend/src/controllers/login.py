from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt
from jose.exceptions import JWTError

from config import get_settings
from schema.user import UserCreate, UserLogin, UserView
from storage import users as UserStorage, NotFoundException

settings = get_settings()

async def authenticate_user(user_login: str, password: str) -> bool:
    password_hash = __hash_password(password)
    try:
        user_password_hash = UserStorage.get_user_password_hash(user_login)
    except NotFoundException:
        return False

    return await UserStorage.authenticate(user_login, password_hash)

async def register(user: UserCreate):
    password_hash = __hash_password(user.password)
    register_date = datetime.now()
    await UserStorage.create(user, password_hash, register_date)

async def get_current_user(token: str) -> Optional[UserView]:
    payload: Optional[dict] = __decode_access_token(token)
    if payload:
        user_login: Optional[str] = payload.get("login")
        if user_login:
            return await UserStorage.get_by_login(login)
    return None

async def login(user: UserLogin) -> Optional[str]:
    if await authenticate_user(user.login, user.password):
        user_view = await UserStorage.get_by_login(user.login)
        token_expires = timedelta(minutes=settings.token_lifetime)
        token = __create_access_token({'login': user_view.login}, token_expires)
        return token
    return None

def __hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def __check_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)

def __create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"expires": expire})
    encoded_jwt = jwt.encode(to_encode, settings.token_secret_key, algorithm=settings.token_algorithm)
    return encoded_jwt

def __decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.token_secret_key, algorithms=settings.token_algorithm)
    except JWTError:
        return None
