from errors import ClientException


class SettingsWriteError(ClientException):
    error_message = """
        An error occured while saving configuration to disk
        Please try again
        {}
    """


class SettingsLoadError(ClientException):
    error_message = """
        Could not found config file
        You need to register the worker first with the "register" command
        {}
    """
