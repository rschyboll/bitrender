"""Contains all errors raised by services, but not related to requests."""
from bitrender.errors import AppError


class ServiceErrors(AppError):
    """Base class for all service error, not related to requests."""


class ContextNotProvided(ServiceErrors):
    """Raised when service was injected, without providing the required context"""
