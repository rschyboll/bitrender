"""Contains base interface for all services."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bitrender.errors.services import ContextNotProvided
from bitrender.services.inject import InjectInService

T = TypeVar("T")


class Service(ABC, Generic[T]):
    """Base class for all services"""

    def __init__(self) -> None:
        super().__init__()
        self.__context: T | None = None
        self.inject = InjectInService(self.__context, "context")

    @abstractmethod
    @property
    def context(self) -> T:
        """Context that needs to be provided, when using this service"""
        if self.__context is None:
            raise ContextNotProvided()
        return self.__context

    @context.setter
    def context(self, value: T) -> None:
        """Setter for the provided context"""
        self.__context = value
        self.inject = InjectInService(self.__context, "context")
