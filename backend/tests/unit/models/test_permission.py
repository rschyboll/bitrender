"""Contains tests for Role model from bitrender.models.role."""
from typing import Any

from tortoise.contrib.test import TruncationTestCase

from bitrender.enums.permission import Permission
from bitrender.models import Role, RolePermission


class TestRolePermission(TruncationTestCase):
    """TestCase containing tests for RolePermission model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.role: Role
        self.permissions = list(Permission)
        self.role_permissions: dict[Permission, RolePermission] = {}

    async def asyncSetUp(self) -> None:
        """Creates database entries used in other tests"""
        await super().asyncSetUp()
        self.role = await Role.create(name="test")
        for permission in self.permissions:
            self.role_permissions[permission] = await RolePermission.create(
                role=self.role, permission=permission
            )

    async def test_permission(self) -> None:
        """Tests returning correctly permission."""
        for permission in self.permissions:
            role_permission = self.role_permissions[permission]
            assert role_permission.permission == permission

    async def test_acl_id(self) -> None:
        """Tests returning correctly acl_id of the permission."""
        for permission in self.permissions:
            role_permission = self.role_permissions[permission]
            assert role_permission.acl_id == permission.acl_id

    async def test_role(self) -> None:
        """Tests returning correctly role of the permission."""
        for role_permission in self.role_permissions.values():
            assert role_permission.role == self.role

    async def test_acl(self) -> None:
        """Tests the __dacl__ and __sacl__ methods."""
        assert len(await RolePermission(permission=Permission.MANAGE_ROLES).__dacl__()) != 0
        assert len(RolePermission.__sacl__()) != 0
