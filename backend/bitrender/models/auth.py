"""TODO generate docstring"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from tortoise.fields import BinaryField, OneToOneRelation

from bitrender.models.base import BaseModel

if TYPE_CHECKING:
    from bitrender.models import User


_MODEL = TypeVar("_MODEL", bound="UserAuth")


class UserAuth(BaseModel):
    """TODO generate docstring"""

    user: OneToOneRelation[User]
    password_hash: bytes = BinaryField()
