from errors import UserError


class NotRegisteredError(UserError):
    pass


class AlreadyRegisteredError(UserError):
    message = """Worker is already registered."""


class RegistrationFailedError(UserError):
    pass
