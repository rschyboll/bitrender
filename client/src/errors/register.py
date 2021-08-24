from errors import ClientException


class NotRegisteredError(ClientException):
    error_message = """
        Worker is not registered, please register using the --register command
        {}
    """


class AlreadyRegisteredError(ClientException):
    error_message = """
        Worker is already registered
        To change server you need to deregister first
        Use the --deregister command to deregister
        {}
    """


class RegistrationFailedError(ClientException):
    error_message = """
        Could not register worker to server
        Please contact the server administrator
        {}
    """


class DeRegistrationFailedError(ClientException):
    error_message = """
        Could not deregister worker from server
        Please contact the server administrator
        {}
    """
