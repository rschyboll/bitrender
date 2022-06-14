from bitrender.errors import AppError


class AuthError(AppError):
    pass


class CredentialsError(AuthError):
    """Raised if the entity requesting a resource has no access to it."""
