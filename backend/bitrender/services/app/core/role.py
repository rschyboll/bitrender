from typing import Any, Coroutine
from uuid import UUID

from antidote import implements
from tortoise.queryset import QuerySet

from bitrender.models import Role, RolePermission
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

    async def get_list(
        self, page: int, count: int, search: str | None, sort: str | None
    ) -> list[str]:
        query: QuerySet[Role]
        if sort is not None:
            query = Role.get_amount(count, page * count, sort, lock=False)
        else:
            query = Role.get_amount(count, page * count, lock=False)
        if search is not None and search != "":
            query = query.filter(name=search)
        roles = await self.auth.query(query, [RolePermission])
        return [role for role in roles]
