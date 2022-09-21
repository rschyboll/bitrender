from bitrender.errors.base import AppError


class UserError(AppError):
    pass


class UserAlreadyExists(UserError):
    pass


class RoleDoesNotExist(UserError):
    pass


class UserDoesNotExist(UserError):
    pass
