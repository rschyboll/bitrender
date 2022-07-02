"""Contains base interface for user services."""
from __future__ import annotations

from abc import ABC

from antidote import interface

from bitrender.services.inject import InjectInService
from bitrender.services.user.context import UserContextProtocol


@interface
class IService(ABC):
    """Base interface for all user services."""

    def __init__(self) -> None:
        self.context: UserContextProtocol
        self.inject_service = InjectInService(self.context, "context")
