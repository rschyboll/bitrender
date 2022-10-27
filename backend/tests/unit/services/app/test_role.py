"""Contains tests for Role model from bitrender.models.role."""
from typing import Any, Literal
from unittest.mock import AsyncMock, MagicMock

import pytest
from antidote import world
from pytest_mock import MockerFixture
from tortoise.contrib.test import TruncationTestCase

from bitrender.models import Role
from bitrender.schemas import RoleView
from bitrender.schemas.list_request import ListRequestInput
from bitrender.services.app.core.role import RoleService


class TestRoleService(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.mocker: MockerFixture

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, mocker: MockerFixture) -> None:
        self.mocker = mocker

    async def test_get_list(self) -> None:
        roles = [Role(name="test"), Role(name="test2")]
        for role in roles:
            await role.save()
        role_views = [await role.to_view() for role in roles]
        request_input = ListRequestInput[Role.columns](sort=None, search=[], page=None)
        service = RoleService()
        self.__mock_role_get_list(roles)
        self.__mock_auth_query(roles)
        returned_role_views = await service.get_list(request_input)
        assert role_views == returned_role_views

    def __mock_role_get_list(self, return_value: list[Any]) -> MagicMock:
        mock = MagicMock()
        mock.return_value.get_list.return_value = return_value
        self.mocker.patch("bitrender.services.app.core.role.Role", mock)
        return mock

    # TODO change mock to injecting to antidote world
    def __mock_auth_service(
        self, return_value: list[Any], error: Exception | None = None
    ) -> MagicMock:
        mock = MagicMock()
        if error is not None:
            mock.return_value.query.side_effect = error
        else:
            async_mock = AsyncMock(return_value=return_value)
            mock.query = async_mock

        return mock
