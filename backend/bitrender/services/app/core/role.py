from antidote import implements

from bitrender.models import Role, RolePermission
from bitrender.schemas import ListRequestInput, RoleView
from bitrender.services.app import IAuthService, IRoleService
from bitrender.services.app.core import BaseAppService


@implements(IRoleService)
class RoleService(BaseAppService, IRoleService):
    """Class that implements the IRoleService, used for operations on roles and permissions"""

    @property
    def auth(self) -> IAuthService:
        """Property for easier accessing the IAuthService, without injecting it in every method

        Returns:
            IAuthService: Injected implementation of the IAuthService interface."""
        auth_service: IAuthService = self.inject(IAuthService)
        return auth_service

    async def get_list(self, request_input: ListRequestInput[Role.columns]) -> list[RoleView]:
        query = Role.get_list(request_input, False).prefetch_related("permissions")
        roles = await self.auth.query(query, [RolePermission])

        return [await role.to_view() for role in roles]
