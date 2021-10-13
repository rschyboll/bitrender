from errors import UserError


class NotRegisteredError(UserError):
    error_message = (
        """Worker is not registered, please register using the --register command"""
    )


class AlreadyRegisteredError(UserError):
    error_message = """
        Worker is already registered
        To change server you need to deregister first
        Use the --deregister command to deregister
    """


class RegistrationFailedError(UserError):
    error_message = """
        Could not register worker to server
        Please contact the server administrator
    """


class DeRegistrationFailedError(UserError):
    error_message = """
        Could not deregister worker from server
        Please contact the server administrator
    """
