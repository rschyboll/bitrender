from fastapi import Depends

from bitrender.auth.deps import get_auth_ids
from bitrender.services.auth import AuthService
from bitrender.services.user import UserService


class Services:
    def __init__(self, auth_ids: list[str] = Depends(get_auth_ids)):
        self.auth = AuthService(self, auth_ids)
        self.user = UserService(self)
