"""Contains all errors related to managing roles."""
from bitrender.errors import AppError


class RoleErrors(AppError):
    """Base class for all errors related to managing roles."""


class RoleNameTaken(RoleErrors):
    """Error raised when a role with the given name exists already."""
