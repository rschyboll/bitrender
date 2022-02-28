from asyncio import AbstractEventLoop, get_event_loop
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from tortoise.contrib.test import finalizer, initializer

from bitrender.config import Settings, get_settings

settings = get_settings()

test_settings = Settings(
    database_url="postgres://postgres:@localhost/bitrender-TEST",
    data_dir="/data-TEST",
)

loop = get_event_loop()


@pytest.fixture(scope="session", autouse=True)
def initialize_orm(request: SubRequest) -> None:
    initializer(
        test_settings.models,
        db_url=test_settings.database_url,
        loop=get_event_loop(),
    )
    request.addfinalizer(finalizer)


@pytest.fixture
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    yield get_event_loop()


def pytest_sessionfinish() -> None:
    get_event_loop().close()
