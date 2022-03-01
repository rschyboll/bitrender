from typing import TYPE_CHECKING

from tortoise.fields.data import BooleanField, TextField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from .base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import Role
else:
    Role = object


"""class User(BaseModel[None]):
    username: str = TextField() 
    full_name: str = TextField()
    email: str = TextField()
    hashed_password: str = TextField()

    active: bool = BooleanField()  # type: ignore
    role: ForeignKeyRelation = ForeignKeyField("models.Role")
"""
