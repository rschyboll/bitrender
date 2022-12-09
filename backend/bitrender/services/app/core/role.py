from uuid import UUID

from antidote import implements
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from bitrender.core.acl import AclAction
from bitrender.errors.role import ReplacementRoleNeeded, RoleIsDefault, RoleNameTaken
from bitrender.models import Role, RolePermission, User
from bitrender.schemas import ListRequestInput, ListRequestOutput, RoleCreate, RoleView
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

    async def get_by_id(self, role_id: UUID) -> RoleView:
        role = await self.auth.query(Role.get_by_id(role_id, False), [RolePermission])
        return await role.to_view()

    async def get_role_users_count(self, role_id: UUID) -> int:
        role = await self.auth.query(Role.get_by_id(role_id, False))
        return await role.users.all().count()

    @atomic()
    async def create(self, role_data: RoleCreate) -> RoleView:
        if await Role.exists(name=role_data.name):
            raise RoleNameTaken()

        if role_data.default:
            await self.__unset_default_role()

        role = await self.auth.action(self.__create_role, AclAction.CREATE, [role_data])
        await self.__create_role_permissions(role_data, role)
        return await role.to_view()

    @atomic()
    async def delete(
        self,
        role_id: UUID,
        replacement_role_id: UUID | None,
    ) -> None:
        role = await Role.get_by_id(role_id)
        if role.default:
            raise RoleIsDefault()
        users = await role.users
        if len(users) != 0 and replacement_role_id is None:
            if replacement_role_id is None or not Role.exists(replacement_role_id):
                raise ReplacementRoleNeeded()
            replacement_role = Role.get_by_id(replacement_role_id)
            await self.__replace_user_roles(users, replacement_role)
        await role.delete()

    async def __replace_user_roles(self, users: list[User], role: Role) -> None:
        for user in users:
            user.role = role
            await user.save()

    async def __unset_default_role(self) -> None:
        default_role = await self.__get_default_role()
        if default_role is not None:
            await self.auth.action(self.__set_role_to_not_default, AclAction.EDIT, [default_role])

    async def __get_default_role(self) -> Role | None:
        try:
            return await Role.get_default()
        except DoesNotExist:
            return None

    async def __set_role_to_not_default(self, role: Role) -> Role:
        pass

    async def __create_role(self, role_data: RoleCreate) -> Role:
        return await Role.create(name=role_data.name)

    async def __create_role_permissions(
        self, role_data: RoleCreate, role: Role
    ) -> list[RolePermission]:
        role_permissions: list[RolePermission] = []
        for permission in role_data.permissions:
            role_permission = await RolePermission.create(permission=permission, role=role)
            role_permissions.append(role_permission)
        return role_permissions
