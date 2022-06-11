from antidote import implements

from bitrender.models import User
from bitrender.services.user.api import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    def get_current(self) -> User:
        pass
