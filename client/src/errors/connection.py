from errors import ClientException


class ConnectionException(ClientException):
    error_message = """
        Can't connect to the server, please check your internet connection
        {}
    """
