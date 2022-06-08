from antidote import implements

from bitrender.services.user.api import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    pass


@implements(IUserService).overriding(UserService)
class UserService2(Service, IUserService):
    pass
