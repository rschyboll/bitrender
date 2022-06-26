"""TODO generate docstring"""
from abc import ABC, abstractmethod

from antidote import implements, inject, interface, wire

from bitrender.services.helpers.interfaces.acl import IACLHelper
from bitrender.services.helpers.interfaces.password import IPasswordHelper
from bitrender.services.helpers.interfaces.token import ITokenHelper


@interface
class IServiceHelpers(ABC):
    """Interface for ServiceHelpers class"""

    @property
    @abstractmethod
    def password(self) -> IPasswordHelper:
        """Returns current IPasswordHelper implementation provided by antidote

        Returns:
            IPasswordHelper: Current implementation of the password helper."""

    @property
    @abstractmethod
    def acl(self) -> IACLHelper:
        """Returns current IACLHelper implementation provided by antidote

        Returns:
            IACLHelper: Current implementation of the acl helper."""

    @property
    @abstractmethod
    def token(self) -> ITokenHelper:
        """Returns current ITokenHelper implementation provided by antidote

        Returns:
            ITokenHelper: Current implementation of the token helper."""


@implements(IServiceHelpers).by_default
@wire
class ServiceHelpers(IServiceHelpers):
    """Container class for all logic helpers not tied to a specific class.

    The class is required, for dependencies in api, that are used by the service classes.
    Without this class, it would create circular dependencies.
    Another soultion would be to remove some of that logic from dependency injection, \
        like the token helper class, but i wanted to keep it so that is also would be injectable.
    Maybe it will be changed in the future to a different solution.

    Properties:
        password: IPasswordServices"""

    def __init__(self):
        self.__password: IPasswordHelper | None = None
        self.__acl: IACLHelper | None = None
        self.__token: ITokenHelper | None = None

    @property
    def password(self) -> IPasswordHelper:
        if self.__password is None:
            return self.__inject_password_helper()
        return self.__password

    def __inject_password_helper(self, password_helper: IPasswordHelper = inject.me()):
        self.__password = password_helper
        return password_helper

    @property
    def acl(self) -> IACLHelper:
        if self.__acl is None:
            return self.__inject_acl_helper()
        return self.__acl

    def __inject_acl_helper(self, acl_helper: IACLHelper = inject.me()):
        self.__acl = acl_helper
        return acl_helper

    @property
    def token(self) -> ITokenHelper:
        if self.__token is None:
            return self.__inject_token_helper()
        return self.__token

    def __inject_token_helper(self, token_helper: ITokenHelper = inject.me()):
        self.__token = token_helper
        return token_helper
