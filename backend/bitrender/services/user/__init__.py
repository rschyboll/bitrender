from abc import ABC, abstractmethod

from antidote import inject, wire
from fastapi import Depends

from bitrender.services.user.context import UserContext
from bitrender.services.user.interfaces.auth import IAuthService
from bitrender.services.user.interfaces.user import IUserService


class IUserServices(ABC):
    """Interface for UserServices class"""

    context: UserContext

    @property
    @abstractmethod
    def user(self) -> IUserService:
        """Returns current IUserService implementation provided by antidote

        Returns:
            IUserService: Current implementation of the user service"""

    @property
    @abstractmethod
    def auth(self) -> IAuthService:
        """Returns current IAuthService implementation provided by antidote

        Returns:
            IAuthService: Current implementation of the authentication service"""


@wire
class UserServices(IUserServices):
    """Container class for all services related to requests made by users

    Allows routes from users api to access services, and allows services to access other services
    All services all injected with the antidote library through their interfaces
    The class is required to connect the FastAPI dependency system with the antidote system

    Properties:
        user: IUserService - implementation of the user service
        auth: IAuthService - implementation of the auth service"""

    def __init__(self, context: UserContext = Depends()):
        self.context = context
        self.__user: IUserService | None = None
        self.__auth: IAuthService | None = None

    @property
    def user(self) -> IUserService:
        if self.__user is None:
            return self.__inject_user_service()
        return self.__user

    def __inject_user_service(self, user_service: IUserService = inject.me()) -> IUserService:
        self.__user = user_service
        user_service.init(self)
        return user_service

    @property
    def auth(self) -> IAuthService:
        if self.__auth is None:
            return self.__inject_auth_service()
        return self.__auth

    def __inject_auth_service(self, auth_service: IAuthService = inject.me()) -> IAuthService:
        self.__auth = auth_service
        auth_service.init(self)
        return auth_service
