from bitrender.errors.base import AppException


class UserException(AppException):
    pass


class NoDefaultRole(UserException):
    pass


class RoleDoesNotExist(UserException):
    pass


class UserAlreadyExist(UserException):
    pass


class BadCredentials(UserException):
    pass


class UserNotVerified(UserException):
    pass
