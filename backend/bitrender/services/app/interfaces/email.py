"""Contains the interface for the email service"""
from abc import ABC

from antidote import interface


@interface
class IEmailService(ABC):
    """Service used for sending emails to users"""
