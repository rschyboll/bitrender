"""Contains tests for Role model from bitrender.models.role."""
from multiprocessing import AuthenticationError
from typing import Any, ContextManager
from unittest.mock import AsyncMock, MagicMock

import pytest
from antidote import world
from antidote.core import TestContextBuilder
from pytest_mock import MockerFixture
from tortoise.contrib.test import TruncationTestCase

from bitrender.models import Role
from bitrender.schemas import RoleView
from bitrender.schemas.list_request import ListRequestInput
from bitrender.services.app.core.role import RoleService
from bitrender.services.app.interfaces.auth import IAuthService
from tests.utils.generators import generate_roles
from tests.utils.mocks import AwaitableMock


class TestRoleService(TruncationTestCase):
    """TestCase containing tests for Role model."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.mocker: MockerFixture
        self.roles_list: list[Role] = []
        self.role_views_list: list[RoleView] = []

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, mocker: MockerFixture) -> None:
        """Injects the mocker fixture into the class attribute."""
        self.mocker = mocker

    async def asyncSetUp(self) -> None:
        """Creates database entries used in tests."""
        await super().asyncSetUp()
        await self.__prepare_role_list()

    async def __prepare_role_list(self) -> None:
        roles = await generate_roles(10)
        self.roles_list = roles
        self.role_views_list = [await role.to_view() for role in roles]

    async def test_get_list(self) -> None:
        """Tests that the get_list method returns and converts correctly the selected roles."""
        request_input = ListRequestInput[Role.columns](sort=None, search=[], page=None)
        service = RoleService()
        with world.test.new() as overrides:
            self.__mock_role_get_list((self.roles_list, len(self.roles_list)))
            overrides[IAuthService] = self.__create_auth_service_mock()
            list_request_output = await service.get_list(request_input)
            assert list_request_output.items == self.role_views_list
            assert list_request_output.row_count == len(self.role_views_list)

    async def test_get_list_auth_error(self) -> None:
        """Tests that the get_list method does not catch errors from the AuthService \
            permission check."""
        request_input = ListRequestInput[Role.columns](sort=None, search=[], page=None)
        service = RoleService()
        with world.test.new() as overrides:
            with pytest.raises(AuthenticationError):
                self.__mock_role_get_list((self.roles_list, len(self.roles_list)))
                overrides[IAuthService] = self.__create_auth_service_mock(AuthenticationError())
                list_request_output = await service.get_list(request_input)
                assert list_request_output.items == self.role_views_list
                assert list_request_output.row_count == len(self.role_views_list)

    async def test_get_list_prefetches_related_models(self) -> None:
        """Tests that the get_list method prefetches related models on the Role model."""
        request_input = ListRequestInput[Role.columns](sort=None, search=[], page=None)
        service = RoleService()
        with world.test.new() as overrides:
            (_, list_query_mock, _) = self.__mock_role_get_list(
                (self.roles_list, len(self.roles_list))
            )
            overrides[IAuthService] = self.__create_auth_service_mock()
            await service.get_list(request_input)
            list_query_mock.prefetch_related.assert_called_once_with("permissions")

    def __mock_role_get_list(
        self, data: tuple[list[Any], int]
    ) -> tuple[MagicMock, AsyncMock, AsyncMock]:
        mock = MagicMock()
        list_mock = AwaitableMock(return_value=data[0])
        count_mock = AwaitableMock(return_value=data[1])
        mock.return_value = (list_mock, count_mock)
        self.mocker.patch("bitrender.services.app.core.role.Role.get_list", mock)
        return mock, list_mock, count_mock

    def __create_auth_service_mock(self, error: Exception | None = None) -> MagicMock:
        mock = MagicMock()
        if error is not None:
            async_mock = AsyncMock(side_effect=error)
            mock.query = async_mock
        else:
            async_mock = AsyncMock(side_effect=self.__await_first_arg)
            mock.query = async_mock
        return mock

    async def __await_first_arg(self, *args: Any) -> Any:
        return await args[0]
