from fastapi import Depends

from bitrender.auth.deps import Auth
from bitrender.services.user import UserService


class Services:
    def __init__(self, auth: Auth = Depends()):
        self.user = UserService(self)
