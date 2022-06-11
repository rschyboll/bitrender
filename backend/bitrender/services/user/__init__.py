from abc import ABC, abstractmethod

from antidote import inject, wire
from fastapi import Depends

from bitrender.services.user.api.user import UserService  # noqa: F401
from bitrender.services.user.context import UserContext
from bitrender.services.user.interfaces.user import IUserService


class IUserServices(ABC):
    """TODO generate docstring"""

    @property
    @abstractmethod
    def user(self) -> IUserService:
        """TODO generate docstring"""


@wire
class UserServices(IUserServices):
    """TODO generate docstring"""

    def __init__(self, context: UserContext = Depends()):
        self.context = context
        self.__user: IUserService | None = None

    @property
    def user(self) -> IUserService:
        if self.__user is None:
            return self.__inject_user_service()
        return self.__user

    def __inject_user_service(self, user_service: IUserService = inject.me()) -> IUserService:
        self.__user = user_service
        user_service.init(self)
        return user_service
