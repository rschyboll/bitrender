"""Contains tests for Role model from bitrender.models.role."""
from __future__ import annotations

from typing import Any

import pytest
from tortoise.contrib.test import TruncationTestCase
from tortoise.exceptions import IntegrityError

from bitrender.enums.permission import Permission
from bitrender.models import Role
from tests.utils.generators import generate_role_permissions, generate_roles, generate_users
from tests.utils.transactions import TransactionTest


class TestRole(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.default_role: Role
        self.custom_roles: list[Role]

    async def asyncSetUp(self) -> None:
        """Creates database entries used in other tests."""
        await super().asyncSetUp()
        self.default_role = await Role.create(name="default", default=True)
        self.custom_roles = await generate_roles(10)

    async def test_get_default(self) -> None:
        """Tests the get_default method with the lock parameter set to False."""
        assert await Role.get_default(False) == self.default_role

    async def test_get_default_lock(self) -> None:
        """Tests the get_default method with the lock parameter set to True."""
        transaction_test = TransactionTest(Role.get_default, (True,), Role.get_all, (True, True))
        default_role, test_roles = await transaction_test()
        assert self.default_role == default_role
        assert default_role not in test_roles
        assert len(test_roles) == len(self.custom_roles)
        assert all(test_role in self.custom_roles for test_role in test_roles)

    async def test_only_one_default(self) -> None:
        """Tests if only one role can be the default one."""
        test_role = self.custom_roles[0]
        with pytest.raises(IntegrityError):
            test_role.default = True
            await test_role.save()
        self.default_role.default = None
        await self.default_role.save()
        test_role.default = True
        await test_role.save()
        assert await Role.get_default(False) == test_role

    async def test_role_permissions(self) -> None:
        """Tests returning correctly roles permissions."""
        counter = 1
        for role in self.custom_roles:
            permissions = [Permission.list()[i] for i in range(0, counter % len(Permission) + 1)]
            role_permissions = await generate_role_permissions(role, permissions)
            selected_role_permissions = await role.permissions
            assert selected_role_permissions == role_permissions
            counter += 1

    async def test_role_users(self) -> None:
        """Tests returning correctly users with the given role."""
        counter = 10
        for role in self.custom_roles:
            users = await generate_users(counter, role)
            selected_users = await role.users
            assert users == selected_users
            counter += 1

    async def test_acl_id_list(self) -> None:
        """Tests acl_id_list property."""
        counter = 1
        for role in self.custom_roles:
            permissions = [Permission.list()[i] for i in range(0, counter % len(Permission) + 1)]
            role_permissions = await generate_role_permissions(role, permissions)
            acl_id_list = [permission.acl_id for permission in role_permissions]
            selected_acl_id_list = await role.acl_id_list
            assert acl_id_list == selected_acl_id_list
            counter += 1

    async def test_to_view(self) -> None:
        """Tests the to_view method."""
        for role in self.custom_roles:
            role_permissions = [
                role_permission.permission for role_permission in await role.permissions
            ]
            role_view = await role.to_view()
            assert role_view.id == role.id
            assert role_view.created_at == role.created_at
            assert role_view.modified_at == role.modified_at
            assert role_view.name == role.name
            assert role_view.default == role.default
            assert role_view.permissions == role_permissions

    async def test_acl(self) -> None:
        """Tests the __dacl__ and __sacl__ methods."""
        assert len(await Role().__dacl__()) != 0
        assert len(Role.__sacl__()) != 0
