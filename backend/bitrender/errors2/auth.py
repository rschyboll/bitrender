from bitrender.errors.base import AppError


class AuthError(AppError):
    pass


class NoDefaultRole(AuthError):
    pass


class BadCredentials(AuthError):
    pass


class CredentialsError(AuthError):
    pass


class UnauthorizedError(AuthError):
    pass


class UserNotVerified(AuthError):
    pass


class AlreadyVerified(AuthError):
    pass


class VerificationFailed(AuthError):
    pass


class TokenError(AuthError):
    pass


class TokenExpiredError(TokenError):
    pass


class TokenCorruptedError(TokenError):
    pass
