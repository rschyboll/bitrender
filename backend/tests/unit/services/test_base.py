"""Contains tests for Service class from bitrender.services.base."""

import pytest

from bitrender.errors.services import (
    BackgroundTasksNotProvided,
    ContextNotProvided,
    SettingsNotProvided,
)
from bitrender.services.base import Service


class TestService(Service[object]):
    """Empty service used only in tests"""


def test_context() -> None:
    """Tests the context property setter and getter."""
    service = TestService()
    service.context = 1
    assert service.context == 1


def test_context_not_set() -> None:
    """Tests that the context property getter raises ContextNotProvided when not set."""
    service = TestService()
    with pytest.raises(ContextNotProvided):
        service.context  # pylint: disable=pointless-statement


def test_context_setattr() -> None:
    """Tests that the context property setter works with the setattr method."""
    service = TestService()
    setattr(service, "context", 1)
    assert service.context == 1


def test_background() -> None:
    """Tests the background property setter and getter."""
    service = TestService()
    service.background = 1
    assert service.background == 1


def test_background_not_set() -> None:
    """Tests that the background property getter raises BackgroundTasksNotProvided when not set."""
    service = TestService()
    with pytest.raises(BackgroundTasksNotProvided):
        service.background  # pylint: disable=pointless-statement


def test_background_setattr() -> None:
    """Tests that the background property setter works with the setattr method."""
    service = TestService()
    setattr(service, "background", 1)
    assert service.background == 1


def test_settings() -> None:
    """Tests the settings property setter and getter."""
    service = TestService()
    service.settings = 1
    assert service.settings == 1


def test_settings_not_set() -> None:
    """Tests that the settings property getter raises SettingsNotProvided when not set."""
    service = TestService()
    with pytest.raises(SettingsNotProvided):
        service.settings  # pylint: disable=pointless-statement


def test_settings_setattr() -> None:
    """Tests that the settings property setter works with the setattr method."""
    service = TestService()
    setattr(service, "settings", 1)
    assert service.settings == 1
