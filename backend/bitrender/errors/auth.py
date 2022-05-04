from bitrender.errors.base import AppError


class AuthError(AppError):
    pass


class UnauthorizedError(AuthError):
    pass


class BadCredentialsError(AuthError):
    pass


class CredentialsError(AuthError):
    pass
