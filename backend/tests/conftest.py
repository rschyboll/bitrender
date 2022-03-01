"""This module contains global fixtures for tests."""
from asyncio import AbstractEventLoop, get_event_loop
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from tortoise.contrib.test import finalizer, initializer

from bitrender.config import Settings, get_settings

settings = get_settings()

test_settings = Settings(
    database_url="postgres://postgres:@localhost:5433/bitrenderTEST",
    data_dir="/data-TEST",
    models=[*settings.models, "tests.unit.models"],
)


@pytest.fixture(scope="session", autouse=True)
def initialize_orm(request: SubRequest) -> None:
    """Initializes database for testing and removes it when finished."""
    initializer(
        test_settings.models,
        db_url=test_settings.database_url,
        loop=get_event_loop(),
    )
    request.addfinalizer(finalizer)


@pytest.fixture
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Returns the current asyncio loop for testing."""
    yield get_event_loop()


def pytest_sessionfinish() -> None:
    """Closes the running loop after all tests."""
    get_event_loop().close()
