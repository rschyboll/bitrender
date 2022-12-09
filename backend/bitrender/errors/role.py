"""Contains all errors related to managing roles."""
from bitrender.errors import AppError


class RoleErrors(AppError):
    """Base class for all errors related to managing roles."""


class RoleNameTaken(RoleErrors):
    """Error raised when a role with the given name exists already."""


class RoleIsDefault(RoleErrors):
    """Error raised when someone attempts to delete a default role, or set a role to not default.

    The system cannot work without a default role, so deleting it is not possible.
    (The system has no roles by default, so it is required by the admin to create one.)

    The only way to change the default role, is to set a different role to default."""


class ReplacementRoleNeeded(RoleErrors):
    """Error raised when someone attempts to delete a role, without providing a replacement role."""


class ReplacementRoleDoesNotExist(RoleErrors):
    """Error raised when the provided replacement role id, does not exist in the database."""
