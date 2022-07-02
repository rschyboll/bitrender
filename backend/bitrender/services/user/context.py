"""Contains all definitions related to shared context of all user services."""
from typing import Protocol

from bitrender.models.user import User


class UserContextProtocol(Protocol):
    current_user: User | None
    auth_ids: list[str]
