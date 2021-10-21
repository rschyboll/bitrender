from errors import UserError


class ConnectionException(UserError):
    message = """Can't connect to server, please check your internet connection.
    If your internet is working, please contact the server administrator."""


class WrongResponseException(UserError):
    message = """The server returned an udefined response.
    Please try again, or contact the server administrator"""
