"""All interface implementations need to be imported in this file to be recognized by antidote."""

from .core.auth import AuthService
from .core.email import EmailService
from .core.role import RoleService
from .core.user import UserService

__all__ = ["AuthService", "UserService", "EmailService", "RoleService"]
