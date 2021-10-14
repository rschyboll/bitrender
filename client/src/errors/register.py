from errors import UserError


class NotRegisteredError(UserError):
    message = (
        """Worker is not registered, please register using the --register command"""
    )


class AlreadyRegisteredError(UserError):
    message = """
        Worker is already registered
        To change server you need to deregister first
        Use the --deregister command to deregister
    """


class RegistrationFailedError(UserError):
    message = """
        Could not register worker to server
        Please contact the server administrator
    """


class DeRegistrationFailedError(UserError):
    message = """
        Could not deregister worker from server
        Please contact the server administrator
    """
