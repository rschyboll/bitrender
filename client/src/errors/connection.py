from errors import UserError


class ConnectionException(UserError):
    message = """Can't connect to the server, please check your internet connection"""
