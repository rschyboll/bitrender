from antidote import implements

from bitrender.models import Role, RolePermission
from bitrender.schemas import ListRequestInput, ListRequestOutput, RoleView
from bitrender.services.app import IAuthService, IRoleService
from bitrender.services.app.core import BaseAppService


@implements(IRoleService)  # type: ignore
class RoleService(BaseAppService, IRoleService):
    """Class that implements the IRoleService, used for operations on roles and permissions"""

    @property
    def auth(self) -> IAuthService:
        """Property for easier accessing the IAuthService, without injecting it in every method

        Returns:
            IAuthService: Injected implementation of the IAuthService interface."""
        auth_service: IAuthService = self.inject(IAuthService)
        return auth_service

    async def get_list(
        self, request_input: ListRequestInput[Role.columns]
    ) -> ListRequestOutput[RoleView]:
        query, count_query = Role.get_list(request_input, False)
        query.prefetch_related("permissions")
        roles = await self.auth.query(query, [RolePermission])

        role_views = [await role.to_view() for role in roles]
        return ListRequestOutput(items=role_views, row_count=await count_query)
