"""Contains tests for User model from bitrender.models.user."""
from typing import Any

import pytest
from tortoise.contrib.test import TruncationTestCase
from tortoise.exceptions import DoesNotExist

from bitrender.enums.permission import Permission
from bitrender.models import Role, User
from tests.utils.generators import generate_role_permissions, generate_roles, generate_users
from tests.utils.transactions import TransactionTest


class TestUser(TruncationTestCase):
    """TestCase containing tests for User model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.default_role_users: list[User]
        self.custom_role_users: list[User]

    async def asyncSetUp(self) -> None:
        """Creates database entries used in other tests."""
        await super().asyncSetUp()
        default_role, custom_role = await self.__prepare_roles()
        self.default_role_users = await generate_users(10, default_role, True, True)
        self.custom_role_users = await generate_users(10, custom_role, True, True)

    @staticmethod
    async def __prepare_roles() -> tuple[Role, Role]:
        default_role = (await generate_roles(1))[0]
        custom_role = (await generate_roles(1))[0]
        default_role.default = True
        await default_role.save()
        await generate_role_permissions(default_role, [Permission.MANAGE_ROLES])
        await generate_role_permissions(
            custom_role, [Permission.MANAGE_ROLES, Permission.MANAGE_USERS]
        )
        return (default_role, custom_role)

    async def test_get_by_username_or_email(self) -> None:
        """Tests the get_by_username_or_email method with the lock parameter set to False."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            db_user_email = await User.get_by_username_or_email(user.email, False)
            db_user_username = await User.get_by_username_or_email(user.username, False)
            assert user == db_user_email
            assert user == db_user_username
        with pytest.raises(DoesNotExist):
            await User.get_by_username_or_email("test")

    async def test_get_by_username_or_email_lock(self) -> None:
        """Tests the get_by_username_or_email method with the lock parameter set to True."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            transaction_test = TransactionTest(
                User.get_by_username_or_email, (user.username, True), User.get_all, (True, True)
            )
            locked_user, not_locked_users = await transaction_test()
            assert user == locked_user
            assert locked_user not in not_locked_users

    async def test_get_by_username(self) -> None:
        """Tests the get_by_username method with the lock parameter set to False."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            db_user = await User.get_by_username(user.username, False)
            assert user == db_user
        with pytest.raises(DoesNotExist):
            await User.get_by_username("test")

    async def test_get_by_username_lock(self) -> None:
        """Tests the get_by_username method with the lock parameter set to True."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            transaction_test = TransactionTest(
                User.get_by_username, (user.username, True), User.get_all, (True, True)
            )
            locked_user, not_locked_users = await transaction_test()
            assert user == locked_user
            assert locked_user not in not_locked_users

    async def test_get_by_email(self) -> None:
        """Tests the get_by_email method with the lock parameter set to False."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            db_user = await User.get_by_email(user.email, False)
            assert user == db_user
        with pytest.raises(DoesNotExist):
            await User.get_by_email("test")

    async def test_get_by_email_lock(self) -> None:
        """Tests the get_by_email method with the lock parameter set to True."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            transaction_test = TransactionTest(
                User.get_by_email, (user.email, True), User.get_all, (True, True)
            )
            locked_user, not_locked_users = await transaction_test()
            assert user == locked_user
            assert locked_user not in not_locked_users

    async def test_acl_id(self) -> None:
        """Tests the acl_id method."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            assert isinstance(user.acl_id, str)
            assert user.acl_id.find(str(user.id)) != -1

    async def test_acl_id_list(self) -> None:
        """Tests the acl_id_list method."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            role = await user.role
            assert set(await user.acl_id_list).issubset(
                set([user.acl_id, *(await role.acl_id_list)])
            )

    async def test_to_view(self) -> None:
        """Tests the to_view method."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            view = await user.to_view()
            role = await user.role
            permissions = [
                role_permission.permission for role_permission in (await role.permissions)
            ]
            assert user.id == view.id
            assert user.created_at == view.created_at
            assert user.modified_at == view.modified_at
            assert user.email == view.email
            assert user.username == view.username
            assert permissions == view.permissions

    async def test_acl(self) -> None:
        """Tests the __dacl__ and __sacl__ methods."""
        for user in [*self.default_role_users, *self.custom_role_users]:
            assert len(await user.__dacl__()) != 0
        assert len(User.__sacl__()) != 0
