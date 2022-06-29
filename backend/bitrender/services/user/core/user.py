from uuid import UUID

from antidote import implements, inject
from tortoise.exceptions import DoesNotExist

from bitrender.core.acl import AclAction
from bitrender.errors.user import (
    CredentialsError,
    NoDefaultRole,
    UnauthenticatedError,
    UserAlreadyExists,
    UserNotActive,
    UserNotVerified,
)
from bitrender.models import Role, RolePermission, User
from bitrender.schemas import UserCreate, UserView
from bitrender.services.helpers import IPasswordHelper, IServiceHelpers
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    async def get_current(self) -> UserView:
        user = self.services.context.current_user
        if user is None:
            raise UnauthenticatedError()
        await self.services.auth.action(
            self.__fetch_user_credentials, AclAction.VIEW, [user], [Role, RolePermission]
        )
        return await user.to_view()

    async def get_by_id(self, user_id: UUID) -> UserView:
        user = await self.services.auth.action(
            self.__fetch_user_with_credentials, AclAction.VIEW, [user_id], [Role, RolePermission]
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

    async def register(self, user_data: UserCreate) -> UserView:
        default_role = await self.__get_default_role()
        return await self.create(user_data, default_role)

    async def create(self, user_data: UserCreate, role: UUID | Role) -> UserView:
        if await User.exists(email=user_data.email):
            raise UserAlreadyExists()
        if not isinstance(role, Role):
            role = await Role.get_by_id(role, False)
        user = await self.services.auth.action(
            self.__create_user, AclAction.CREATE, [user_data, role]
        )
        return await user.to_view()

    @inject
    async def __create_user(
        self,
        user_data: UserCreate,
        role: Role,
        password_helper: IPasswordHelper = inject.me(),
    ) -> User:
        hashed_password = password_helper.hash(user_data.password)
        user = await User.create(email=user_data.email, hashed_password=hashed_password, role=role)
        return user

    async def __get_default_role(self) -> Role:
        try:
            return await Role.get_default(False)
        except DoesNotExist as error:
            raise NoDefaultRole() from error

    async def __fetch_user_with_credentials(self, user_id: UUID) -> User:
        user = await User.get_by_id(user_id)
        await self.__fetch_user_credentials(user)
        return user

    async def __fetch_user_credentials(self, user: User) -> User:
        await user.fetch_related("role__permissions")
        return user
