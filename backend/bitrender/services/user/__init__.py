from antidote import inject, wire
from fastapi import Depends

from bitrender.api.deps.user import get_current_user_or_none
from bitrender.models.user import User
from bitrender.services.user.api.user import UserService
from bitrender.services.user.interfaces.user import IUserService


class IUserServices:
    user_service: IUserService


@wire
class UserServices:
    def __init__(self, user: User = Depends(get_current_user_or_none)):
        self.current_user = user
        self.__user_service: IUserService | None = None

    @property
    def user_service(self) -> IUserService:
        if self.__user_service is None:
            return self.__inject_user_service()
        return self.__user_service

    def __inject_user_service(self, user_service: IUserService = inject.me()) -> IUserService:
        self.__user_service = user_service
        user_service.init(self)
        return user_service
