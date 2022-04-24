"""TODO generate docstring"""


from pydantic import BaseModel as PydanticBase
from pydantic import EmailStr, SecretStr, validator

from bitrender.auth.password import validate_password
from bitrender.schemas.base import BaseSchema


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
        validate_password(password)
