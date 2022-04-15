"""Contains tests for Role model from bitrender.models.role."""
from __future__ import annotations

import pytest
from tortoise.contrib.test import TruncationTestCase
from tortoise.exceptions import IntegrityError

from bitrender.models import Permission, Role, RolePermission
from tests.utils import TransactionTest


class TestRole(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_role: Role = Role(name="default", default=True)
        self.custom_roles = [Role(name=str(i)) for i in range(0, 10)]

    async def asyncSetUp(self):
        """Creates database entries used in other tests"""
        await super().asyncSetUp()
        await self.default_role.save()
        for role in self.custom_roles:
            await role.save()

    async def test_get_default(self):
        """Tests the get_default method with lock set to False."""
        assert await Role.get_default(False) == self.default_role

    async def test_get_default_lock(self):
        """Tests the get_default method with lock set to True."""
        transaction_test = TransactionTest(Role.get_default, (True,), Role.get_all, (True, True))
        default_role, test_roles = await transaction_test()
        assert self.default_role == default_role
        assert default_role not in test_roles
        assert len(test_roles) == len(self.custom_roles)
        assert all(test_role in self.custom_roles for test_role in test_roles)

    async def test_only_one_default(self):
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

    @staticmethod
    async def __create_permissions(role: Role, permissions: list[Permission]):
        for permission in permissions:
            role_permission = RolePermission(permission=permission, role=role)
            await role_permission.save()

    async def test_role_permissions(self):
        """Tests returning correctly roles permissions."""
        all_permissions = [permission for permission in Permission]
        permission_counter = 1
        for role in self.custom_roles:
            permissions = [
                all_permissions[i]
                for i in range(
                    permission_counter % len(all_permissions),
                    len(all_permissions),
                )
            ]
            await self.__create_permissions(role, permissions)
            selected_role_permissions = await role.permissions
            assert len(permissions) == len(selected_role_permissions)
            assert all(
                role_permission.permission in permissions
                for role_permission in selected_role_permissions
            )
            permission_counter += 1

    async def test_acl_id_list(self):
        """Tests acl_id_list property."""
        all_permissions = [permission for permission in Permission]
        permission_counter = 1
        for role in self.custom_roles:
            permissions = [
                all_permissions[i]
                for i in range(
                    permission_counter % len(all_permissions),
                    len(all_permissions),
                )
            ]
            acl_id_list = [permission.acl_id for permission in permissions]
            await self.__create_permissions(role, permissions)
            selected_acl_id_list = await role.acl_id_list
            assert len(acl_id_list) == len(selected_acl_id_list)
            assert all(acl_id in acl_id_list for acl_id in selected_acl_id_list)
            permission_counter += 1
