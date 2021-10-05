from errors import UserException


class NotRegisteredError(UserException):
    error_message = (
        """Worker is not registered, please register using the --register command"""
    )


class AlreadyRegisteredError(UserException):
    error_message = """
        Worker is already registered
        To change server you need to deregister first
        Use the --deregister command to deregister
    """


class RegistrationFailedError(UserException):
    error_message = """
        Could not register worker to server
        Please contact the server administrator
    """


class DeRegistrationFailedError(UserException):
    error_message = """
        Could not deregister worker from server
        Please contact the server administrator
    """
