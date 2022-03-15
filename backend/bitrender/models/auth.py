from typing import TYPE_CHECKING, TypeVar

from tortoise.fields import BinaryField, OneToOneRelation
from tortoise.models import Model

if TYPE_CHECKING:
    from bitrender.models import User
else:
    User = object

_MODEL = TypeVar("_MODEL", bound="UserAuth")


class UserAuth(Model):
    """TODO generate docstring"""

    user: OneToOneRelation[User]
    password_hash: bytes = BinaryField()
