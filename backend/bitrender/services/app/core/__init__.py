"""Contains user service implementation."""

from bitrender.services import Service
from bitrender.services.app.context import WebContextProtocol


class BaseAppService(Service[WebContextProtocol]):
    """TODO generate docstring"""

    def __init__(self) -> None:
        super().__init__()
