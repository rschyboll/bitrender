"""Contains all definitions related to shared context of all user services"""
from typing import Protocol

from bitrender.models.user import User


class WebContextProtocol(Protocol):
    """Context required to use user services
    Attributes:
        current_user (User | None): Current user who made the request
        auth_ids (list[str]): Authentication ids from the current user"""

    current_user: User | None
    auth_ids: list[str]
