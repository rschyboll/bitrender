from uuid import UUID

from antidote import implements, inject
from tortoise.exceptions import DoesNotExist

from bitrender.core.acl import AclAction
from bitrender.errors.user import (
    CredentialsError,
    UnauthenticatedError,
    UserNotActive,
    UserNotVerified,
)
from bitrender.models import Role, RolePermission, User
from bitrender.schemas import UserView
from bitrender.services.helpers import IServiceHelpers
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    async def get_current(self) -> UserView:
        user = self.services.context.current_user
        if user is None:
            raise UnauthenticatedError()
        await self.services.auth.action(
            self.__fetch_user_credentials, AclAction.VIEW, (user,), [Role, RolePermission]
        )
        return await user.to_view()

    async def get_by_id(self, user_id: UUID) -> UserView:
        user = await self.services.auth.action(
            self.__fetch_user_with_credentials, AclAction.VIEW, (user_id,), [Role, RolePermission]
        )
        return await user.to_view()

    async def authenticate(
        self,
        email: str,
        password: str,
        helpers: IServiceHelpers = inject.me(),
    ) -> str:
        try:
            user = await User.get_by_email(email)
        except DoesNotExist as error:
            raise CredentialsError() from error
        if not user.is_verified:
            raise UserNotVerified()
        if not user.is_active:
            raise UserNotActive()
        if helpers.password.verify(password, user.hashed_password):
            return helpers.token.create_user_token(user.id)
        raise CredentialsError()

    async def __fetch_user_with_credentials(self, user_id: UUID) -> User:
        user = await User.get_by_id(user_id)
        await self.__fetch_user_credentials(user)
        return user

    async def __fetch_user_credentials(self, user: User) -> User:
        await user.fetch_related("role__permissions")
        return user
