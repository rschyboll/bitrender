from antidote import implements

from bitrender.core.acl import AclAction
from bitrender.models import Role, RolePermission, User
from bitrender.schemas import UserView
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    async def get_current(self) -> UserView | None:
        user = self.services.context.current_user
        if user is None:
            return None
        await self.services.auth.action(
            self.__fetch_user_data, AclAction.VIEW, (user,), [Role, RolePermission]
        )
        return await user.to_view()

    @staticmethod
    async def __fetch_user_data(user: User) -> User:
        await user.fetch_related("role__permissions")
        return user
