"""Contains all definitions related to shared context of all user services."""
from fastapi import Depends

from bitrender.api.deps.user import get_auth_ids, get_current_user_or_none
from bitrender.models.user import User


class UserContext:
    """User services context, contains all dependencies shared by all routes using user serivices.

    Attributes:
        current_user (User, optional): Current user that send the request.
        auth_ids (list[str]): Authentication ids of the current user."""

    def __init__(
        self,
        current_user: User = Depends(get_current_user_or_none),
        auth_ids: list[str] = Depends(get_auth_ids),
    ) -> None:
        self.current_user: User = current_user
        self.auth_ids: list[str] = auth_ids
