"""Contains base interface for user services."""
from __future__ import annotations

from typing import TYPE_CHECKING

from antidote import interface

if TYPE_CHECKING:
    from bitrender.services.user import IUserServices


@interface
class IService:
    """Base interface for all user services."""

    services: IUserServices

    def init(self, services: IUserServices):
        """Initializes the service and injects the services instance"""
