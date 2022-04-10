from uuid import UUID

from pydantic import BaseModel as Schema
from pydantic import EmailStr, SecretStr

from bitrender.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    username: str
    email: EmailStr
    active: bool


class UserSchemaFlat(UserSchema):
    role_id: UUID


class UserSchemaPartial(BaseSchema):
    pass


class UserSchemaFull(BaseSchema):
    pass


class UserRegisterData(Schema):
    username: str
    email: EmailStr
    password: SecretStr


class UserLoginData(Schema):
    username_email: str | EmailStr
    password: SecretStr
