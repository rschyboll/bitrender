from bitrender.errors.base import AppError


class UserError(AppError):
    pass


class NoDefaultRoleError(UserError):
    pass


class RoleDoesNotExistError(UserError):
    pass


class UserAlreadyExistError(UserError):
    pass


class UserNotVerifiedError(UserError):
    pass
