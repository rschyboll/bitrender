"""TODO generate docstring"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bitrender.config import Settings

if TYPE_CHECKING:
    from bitrender.services import Services


class EmailService:
    """TODO generate docstring"""

    def __init__(self, services: Services, settings: Settings):
        self.services = services
        self.settings = settings
        self.logger = logging.getLogger()

    async def send_verify_email(self, email: str, token: str):
        self.logger.info(f"Verify email send to: {email} with token {token}")
