from errors import UserError


class ConnectionException(UserError):
    message = """Can't connect to server, please check your internet connection.
    If your internet is working, please contact the server administrator."""
