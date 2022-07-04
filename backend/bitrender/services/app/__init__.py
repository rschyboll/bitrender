"""Reexports all user service interfaces"""
from bitrender.services.app.interfaces.auth import IAuthService
from bitrender.services.app.interfaces.user import IUserService

__all__ = ["IAuthService", "IUserService"]
