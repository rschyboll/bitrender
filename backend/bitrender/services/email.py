"""TODO generate docstring"""
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from bitrender.config import Settings

if TYPE_CHECKING:
    from bitrender.services import Services


class EmailService:
    """TODO generate docstring"""

    def __init__(self, services: Services, settings: Settings):
        self.services = services
        self.settings = settings
        self.mail = FastMail(self.__get_config(settings))

    async def send_verify_email(self, email: str, token: str):
        message = MessageSchema(
            subject="Test", recipients=["hoodrobin.rs@gmail.com"], body="TEST", subtype="html"
        )
        await self.mail.send_message(message)

    async def send_reset_email(self, email: str, token: str):
        message = MessageSchema(
            subject="Test", recipients=["hoodrobin.rs@gmail.com"], body="TEST", subtype="html"
        )
        await self.mail.send_message(message)

    @staticmethod
    def __get_config(settings: Settings) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=settings.email_username,
            MAIL_PASSWORD=settings.email_password,
            MAIL_FROM=settings.email_from,
            MAIL_PORT=settings.email_port,
            MAIL_SERVER=settings.email_server,
            MAIL_TLS=settings.email_tls,
            MAIL_SSL=settings.email_ssl,
        )
