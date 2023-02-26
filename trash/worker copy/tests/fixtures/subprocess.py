"""This module contains fixtures for asyncio.subprocess."""

import pytest
from pytest_mock import MockerFixture

from tests.mocks.subprocess import MockProcess


@pytest.fixture
def process(
    mocker: MockerFixture,
    process_mock_path: str = "bitrender_worker.utils.subprocess.create_subprocess_exec",
) -> MockProcess:
    """Fixture for mocking Process returned from asyncio.create_subprocess_exec."""
    mock = mocker.patch(process_mock_path)
    mock.return_value = MockProcess()
    return mock.return_value
