"""Contains tests for Role model from bitrender.models.role."""
from __future__ import annotations

from tortoise.contrib.test import TruncationTestCase

from bitrender.models import Permission, Role
from bitrender.models.permission import RolePermission


class TestRolePermission(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role: Role
        self.permissions = list(Permission)
        self.role_permissions: dict[Permission, RolePermission] = {}

    async def asyncSetUp(self):
        """Creates database entries used in other tests"""
        await super().asyncSetUp()
        self.role = await Role.create(name="test")
        for permission in self.permissions:
            self.role_permissions[permission] = await RolePermission.create(
                role=self.role, permission=permission
            )

    async def test_permission(self):
        """Tests returning correctly permission."""
        for permission in self.permissions:
            role_permission = self.role_permissions[permission]
            assert role_permission.permission == permission

    async def test_acl_id(self):
        """Tests returning correctly acl_id of the permission."""
        for permission in self.permissions:
            role_permission = self.role_permissions[permission]
            assert role_permission.acl_id == permission.acl_id

    async def test_role(self):
        """Tests returning correctly role of the permission."""
        for role_permission in self.role_permissions.values():
            assert role_permission.role == self.role
