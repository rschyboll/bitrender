"""This module contains global fixtures for tests."""

import pytest
from _pytest.fixtures import SubRequest
from tortoise.contrib.test import finalizer, initializer

from bitrender.config import Settings, get_settings

settings = get_settings()

test_settings = Settings(
    database_url="postgres://postgres:@localhost:5433/bitrender-TEST",
    data_dir="/data-TEST",
    models=[*settings.models, "tests.unit.models"],
)


@pytest.fixture(scope="session", autouse=True)
def initialize_orm(request: SubRequest) -> None:
    """Initializes database for testing and removes it when finished."""
    initializer(test_settings.models, db_url=test_settings.database_url, app_label="bitrender")
    request.addfinalizer(finalizer)
