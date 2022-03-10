from typing import TYPE_CHECKING, Type, TypeVar

from tortoise.fields import (
    BinaryField,
    BooleanField,
    ForeignKeyField,
    ForeignKeyRelation,
    TextField,
)

from bitrender.models.base import BaseModel
from bitrender.schemas import UserView

if TYPE_CHECKING:
    from bitrender.models import Role
else:
    Role = object

_MODEL = TypeVar("_MODEL", bound="User")


class User(BaseModel[UserView]):
    username: str = TextField(unique=True)
    password_hash: bytes = BinaryField()
    email: str = TextField(unique=True)

    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> UserView:
        """Converts the model to it's corresponding pydantic schema."""
        return UserView.from_orm(self)

    @classmethod
    async def get_by_username(cls: Type[_MODEL], username: str) -> _MODEL:
        return await cls.get(username=username)
