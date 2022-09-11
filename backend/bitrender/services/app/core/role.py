from typing import Any, Coroutine, Generic, Literal, TypeVar
from uuid import UUID

from antidote import implements
from tortoise.queryset import QuerySet

from bitrender.models import Role, RolePermission
from bitrender.schemas import ListRequestInput
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

    async def get_list(self, request_input: ListRequestInput[Role.columns]) -> list[Role]:
        query = Role.get_list(request_input, False)

        test: ListRequestInput[Role.columns] = 1
        test2: ListRequestInput[str] = test

        test3 = test2

        return await self.auth.query(query, [RolePermission])


T = TypeVar("T")


class Test(Generic[T]):
    pass


def test(test: Test[str ]):
    pass


test2: Test[Literal["str"]] = Test()


test(test2)
