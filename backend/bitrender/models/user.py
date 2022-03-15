from typing import TYPE_CHECKING, Literal, Type, TypeVar, overload

from tortoise.fields import (
    BooleanField,
    CharField,
    ForeignKeyField,
    ForeignKeyRelation,
    OneToOneField,
    OneToOneNullableRelation,
)

from bitrender.models.base import BaseModel
from bitrender.schemas import UserView

if TYPE_CHECKING:
    from bitrender.models import Role, UserAuth
else:
    Role = object
    UserAuth = object

_MODEL = TypeVar("_MODEL", bound="User")


class User(BaseModel[UserView]):
    """TODO create docstring"""

    username: str = CharField(32, unique=True)
    email: str = CharField(255, unique=True)

    auth: OneToOneNullableRelation[UserAuth] = OneToOneField(
        "bitrender.UserAuth", null=True, default=None
    )
    role: ForeignKeyRelation[Role] = ForeignKeyField("bitrender.Role")

    removable: bool = BooleanField(default=True)  # type: ignore

    def to_view(self) -> UserView:
        """Converts the model to it's corresponding pydantic schema."""
        return UserView.from_orm(self)

    @overload
    @classmethod
    async def get_by_username(
        cls: Type[_MODEL], username: str, view: Literal[False] = ...
    ) -> _MODEL:
        ...

    @overload
    @classmethod
    async def get_by_username(cls: Type[_MODEL], username: str, view: Literal[True]) -> UserView:
        ...

    @classmethod
    async def get_by_username(
        cls: Type[_MODEL], username: str, view: bool = False
    ) -> _MODEL | UserView:
        """Returns a user based on provided username.

        Args:
            view (bool, optional): Specifies if the model should be converted to it's schema.
                Defaults to False.

        Returns:
            _MODEL: If view is False. Instance of the user model.
                Locks the row in the database.
            UserView: If view if True. Schema created from the user model.
                Does not lock the row in the database."""
        if not view:
            return await cls.select_for_update().get(username=username)
        return (await cls.get(username=username)).to_view()
