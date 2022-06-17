from abc import abstractmethod

from antidote import interface

from bitrender.schemas import UserView

from . import IService


@interface
class IUserService(IService):
    """TODO generate docstring"""

    @abstractmethod
    async def get_current(self) -> UserView | None:
        """TODO generate docstring"""
