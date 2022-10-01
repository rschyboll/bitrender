"""Contains user service implementation."""

from bitrender.services.app.context import WebContextProtocol
from bitrender.services.base import Service


class BaseAppService(Service[WebContextProtocol]):
    """TODO generate docstring"""

    def __init__(self) -> None:
        super().__init__()
