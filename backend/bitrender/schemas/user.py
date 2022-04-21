"""TODO generate docstring"""

from pydantic import BaseModel as PydanticBase
from pydantic import EmailStr, SecretStr, validator

from bitrender.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    """TODO generate docstring"""

    email: EmailStr


class UserRegister(PydanticBase):
    """TODO generate docstring"""

    email: EmailStr
    password: SecretStr

    @staticmethod
    @validator("password")
    def password_check(password: str):
        """Validates that the password is secure enough."""
        if len(password) < 8:
            raise ValueError("Password length should be at least 8")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            raise ValueError("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise ValueError("Password should have at least one lowercase letter")
