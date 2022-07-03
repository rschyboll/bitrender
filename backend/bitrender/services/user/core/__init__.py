"""Contains user service implementation."""

from bitrender.services import Service
from bitrender.services.user.context import UserContextProtocol


class BaseUserService(Service[UserContextProtocol]):
    """TODO generate docstring"""

    def __init__(self) -> None:
        super().__init__()
