from uuid import UUID

from antidote import implements, inject, world
from tortoise.exceptions import DoesNotExist

from bitrender.core.acl import AclAction
from bitrender.errors.user import (
    BadCredentials,
    EmailTaken,
    NoDefaultRole,
    UnauthenticatedError,
    UsernameTaken,
    UserNotVerified,
)
from bitrender.models import Role, RolePermission, User
from bitrender.schemas import UserCreate, UserView
from bitrender.services.app import IAuthService, IUserService
from bitrender.services.app.core import BaseAppService
from bitrender.services.helpers import IPasswordHelper, ITokenHelper


@implements(IUserService)  # type: ignore
class UserService(BaseAppService, IUserService):
    @property
    def password(self) -> IPasswordHelper:
        """Property for easier accessing the IPasswordHelper, without injecting it in every method

        Returns:
            IPasswordHelper: Injected implementation of the IPasswordHelper interface."""
        password_helper: IPasswordHelper = world.get(IPasswordHelper)  # type: ignore
        return password_helper

    @property
    def token(self) -> ITokenHelper:
        """Property for easier accessing the ITokenHelper, without injecting it in every method

        Returns:
            ITokenHelper: Injected implementation of the ITokenHelper interface."""
        token_helper: ITokenHelper = world.get(ITokenHelper)  # type: ignore
        return token_helper

    @property
    def auth(self) -> IAuthService:
        """Property for easier accessing the IAuthService, without injecting it in every method

        Returns:
            IAuthService: Injected implementation of the IAuthService interface."""
        auth_service: IAuthService = self.inject(IAuthService)
        return auth_service

    async def get_current(self) -> UserView:
        user = self.context.current_user
        if user is None:
            raise UnauthenticatedError()
        if not user.is_active or not user.is_verified:
            raise UnauthenticatedError()
        await self.auth.action(
            self.__fetch_user_credentials, AclAction.VIEW, [user], [Role, RolePermission]
        )
        return await user.to_view()

    async def logged(self) -> bool:
        user = self.context.current_user
        if user is not None and user.is_active and user.is_verified:
            return True
        return False

    async def get_by_id(self, user_id: UUID) -> UserView:
        user = await self.auth.action(
            self.__fetch_user_with_credentials, AclAction.VIEW, [user_id], [Role, RolePermission]
        )
        return await user.to_view()

    async def authenticate(self, username: str, password: str) -> str:
        try:
            user = await User.get_by_username_or_email(username)
        except DoesNotExist as error:
            raise BadCredentials() from error
        if not user.is_verified:
            raise UserNotVerified()
        if not user.is_active:
            raise BadCredentials()
        if self.password.verify(password, user.hashed_password):
            return self.token.create_user_token(user.id)
        raise BadCredentials()

    async def register(self, user_data: UserCreate) -> UserView:
        default_role = await self.__get_default_role()
        return await self.create(user_data, default_role)

    async def create(self, user_data: UserCreate, role: UUID | Role) -> UserView:
        if await User.exists(email=user_data.email):
            raise EmailTaken()
        if await User.exists(username=user_data.username):
            raise UsernameTaken()
        if not isinstance(role, Role):
            role = await Role.get_by_id(role, False)
        user = await self.auth.action(self.__create_user, AclAction.CREATE, [user_data, role])
        return await user.to_view()

    @inject
    async def __create_user(
        self,
        user_data: UserCreate,
        role: Role,
        password_helper: IPasswordHelper = inject.me(),
    ) -> User:
        hashed_password = password_helper.hash(user_data.password.get_secret_value())
        user = await User.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=role,
        )
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
        await user.fetch_related("role")
        await (await user.role).fetch_related("permissions")
        return user
