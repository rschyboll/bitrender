"""Contains base interface for user services."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from antidote import interface

if TYPE_CHECKING:
    from bitrender.services.user import IUserServices


@interface
class IService(ABC):
    """Base interface for all user services."""

    @property
    @abstractmethod
    def services(self) -> IUserServices:
        """Instance of IUserSevices class for accessing other services"""

    @abstractmethod
    def init(self, services: IUserServices):
        """Initializes the service and injects the services instance"""
