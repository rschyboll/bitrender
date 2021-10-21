import os
import random
import string
from typing import Generator, Type
from unittest import mock

import pytest

from config import DIR, URL, Settings
from errors.config import SettingsNotReadError, SettingsReadError, SettingsWriteError


@pytest.fixture(scope="function")
def settings(self, tmpdir: str) -> Settings:
    return Settings(os.path.join(tmpdir, self.settings_file))


def test_set_option(self) -> None:
    pass
