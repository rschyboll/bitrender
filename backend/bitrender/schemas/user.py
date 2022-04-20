"""TODO generate docstring"""

from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from bitrender.models import User


class UserSchema(models.BaseUser):
    """TODO generate docstring"""


class UserCreate(models.BaseUserCreate):
    """TODO generate docstring"""


class UserUpdate(models.BaseUserUpdate):
    """TODO generate docstring"""


class UserAuth(UserSchema, models.BaseUserDB, PydanticModel):
    """TODO generate docstring"""

    class Config:
        """TODO generate docstring"""

        orm_mode = True
        orig_model = User
