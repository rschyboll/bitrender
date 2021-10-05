from errors import UserException


class ConnectionException(UserException):
    message = """Can't connect to the server, please check your internet connection"""
