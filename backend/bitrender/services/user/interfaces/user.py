from abc import abstractmethod

from antidote import interface

from bitrender.models import User

from . import IService


@interface
class IUserService(IService):
    """TODO generate docstring"""

    @abstractmethod
    def get_current(self) -> User:
        """TODO generate docstring"""
