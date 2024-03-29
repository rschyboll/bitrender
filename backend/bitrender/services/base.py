"""Contains base interface for all services."""
from __future__ import annotations

from abc import ABC
from typing import Any, Callable, Generic, Protocol, TypeVar

from bitrender.errors.services import (
    BackgroundTasksNotProvided,
    ContextNotProvided,
    SettingsNotProvided,
)
from bitrender.services.inject import InjectInService

T = TypeVar("T")


class BackgroundTasksProtocol(Protocol):
    """Protocol for a class for launching background tasks."""

    def add_task(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Function for launching tasks in the background."""


class SettingsProtocol(Protocol):
    """Protocol for settings loaded from env"""

    email_username: str
    email_password: str
    email_from: str
    email_port: int
    email_server: str
    email_tls: bool
    email_ssl: bool


class Service(ABC, Generic[T]):
    """Base class for all services"""

    def __init__(self) -> None:
        super().__init__()
        self.__context: T | None = None
        self.__background: BackgroundTasksProtocol | None = None
        self.__settings: SettingsProtocol | None = None
        self.inject = InjectInService(self.__context, "context")

    @property
    def context(self) -> T:
        """Context that needs to be provided, when using this service"""
        if self.__context is None:
            raise ContextNotProvided()
        return self.__context

    @context.setter
    def context(self, value: T) -> None:
        """Setter for the services context"""
        self.__context = value
        self.inject = InjectInService(self.__context, "context")

    @property
    def background(self) -> BackgroundTasksProtocol:
        """Background tasks instance, that needs to be provided when using this service.
        Used for launching background tasks from services."""
        if self.__background is None:
            raise BackgroundTasksNotProvided()
        return self.__background

    @background.setter
    def background(self, value: BackgroundTasksProtocol) -> None:
        """Setter for the background property"""
        self.__background = value

    @property
    def settings(self) -> SettingsProtocol:
        """Settings instance, used by services to get the required config."""
        if self.__settings is None:
            raise SettingsNotProvided()
        return self.__settings

    @settings.setter
    def settings(self, value: SettingsProtocol) -> None:
        self.__settings = value
