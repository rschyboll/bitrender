from uuid import UUID

from antidote import implements

from bitrender.services.app import IAuthService, IRoleService
from bitrender.services.app.core import BaseAppService


@implements(IRoleService).by_default
class RoleService(BaseAppService, IRoleService):
    @property
    def auth(self) -> IAuthService:
        """Property for easier accessing the IAuthService, without injecting it in every method

        Returns:
            IAuthService: Injected implementation of the IAuthService interface."""
        auth_service: IAuthService = self.inject(IAuthService)
        return auth_service

    def get_list(self, page: int, count: int) -> list[str]:
        pass
