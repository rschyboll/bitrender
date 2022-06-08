from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bitrender.services.user import UserServices


class UserService:
    def __init__(self, services: UserServices):
        pass
