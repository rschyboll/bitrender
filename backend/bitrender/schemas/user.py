from pydantic import BaseModel as Schema
from pydantic import EmailStr, SecretStr

from bitrender.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    username: str
    email: EmailStr
    active: bool


class UserRegisterData(Schema):
    username: str
    email: EmailStr
    password: SecretStr


class UserLoginData(Schema):
    login: str | EmailStr
    password: SecretStr
