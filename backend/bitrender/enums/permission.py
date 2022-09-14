"""Contains enums for models and schemas describing user permissions."""
from __future__ import annotations

from enum import Enum, unique


@unique
class Permission(Enum):
    """Static enum containing available user permissions."""

    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"

    @property
    def acl_id(self) -> str:
        """TODO generate docstring"""
        return f"permission:{self.value}"

    @classmethod
    def list(cls) -> list[Permission]:
        """TODO generate docstring"""
        return list(Permission)
