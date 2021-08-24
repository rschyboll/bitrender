from typing import Optional


class ClientException(Exception):
    error_message = ""

    def __init__(self, *args: object, message: Optional[str] = None):
        super(ClientException, self).__init__(args)
        self.message = message

    def __str__(self) -> str:
        if self.message is None:
            return self.error_message.format("")
        return self.error_message.format(self.message)


class UndefinedException(ClientException):
    error_message = """
        An undefined exception has occured
        Error message: {}
    """
