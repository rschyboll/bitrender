"""Contains user service implementation."""
from typing import TYPE_CHECKING

from antidote import implements

from bitrender.services.user.interfaces import IService

if TYPE_CHECKING:
    from bitrender.services.user import IUserServices
else:
    IUserServices = object


@implements(IService)
class Service(IService):
    def __init__(self, services: IUserServices | None = None):
        self.__services = services

    def init(self, services: IUserServices):
        self.__services = services

    @property
    def services(self) -> IUserServices:
        if self.__services is None:
            raise Exception()
        return self.__services
