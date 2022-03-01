from tortoise.fields.data import TextField

from bitrender.schemas.role import RoleView

from .base import BaseModel


class Role(BaseModel[RoleView]):
    name: str = TextField()
