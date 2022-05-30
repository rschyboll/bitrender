"""TODO generate docstring"""


from pydantic import BaseModel as PydanticBase
from pydantic import EmailStr, SecretStr, validator

from bitrender.auth.password import PasswordHelper
from bitrender.models.permission import Permission
from bitrender.schemas.base import BaseSchema


class UserView(BaseSchema):
    """Class containing all user data required for the frontend."""

    email: EmailStr
    role: str
    permissions: list[Permission]


class UserSchema(BaseSchema):
    """TODO generate docstring"""

    email: EmailStr


class UserCreate(PydanticBase):
    """TODO generate docstring"""

    email: EmailStr
    password: SecretStr

    @staticmethod
    @validator("password")
    def password_check(password: str):
        """Validates that the password is secure enough."""
        PasswordHelper.validate(password)
