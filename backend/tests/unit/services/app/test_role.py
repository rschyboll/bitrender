"""Contains tests for Role model from bitrender.models.role."""
from typing import Any

from tortoise.contrib.test import TruncationTestCase

from bitrender.services.app.core.role import RoleService


class TestRoleService(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def asyncSetUp(self) -> None:
        """Creates database entries used in other tests"""
        await super().asyncSetUp()

    async def test_get_list(self) -> None:
        pass

    async def __mock_role_get_list(self) -> None:
        pass

    async def __mock_auth_query(self) -> None:
        pass
