from dependency_injector import containers, providers

from bitrender.services.interfaces.user import IUserService
from bitrender.services.user import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client: providers.Provider[IUserService] = providers.Singleton(UserService)
