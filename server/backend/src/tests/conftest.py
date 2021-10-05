import os
import shutil
from asyncio import AbstractEventLoop, get_event_loop
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from tortoise.contrib.test import finalizer, initializer

from config import get_settings

settings = get_settings()


@pytest.fixture(scope="session", autouse=True)
def initialize_orm(request: SubRequest) -> None:
    initializer(
        settings.models,
        db_url=settings.postgres_test_database_url,
        loop=get_event_loop(),
    )
    request.addfinalizer(finalizer)


@pytest.fixture(scope="function", autouse=True)
def create_temp_task_folder(request: SubRequest) -> None:
    os.makedirs(settings.task_files_path, exist_ok=True)

    def delete_temp_task_folder() -> None:
        shutil.rmtree(settings.task_files_path)

    request.addfinalizer(delete_temp_task_folder)


@pytest.fixture
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    yield get_event_loop()


def pytest_sessionfinish() -> None:
    get_event_loop().close()
