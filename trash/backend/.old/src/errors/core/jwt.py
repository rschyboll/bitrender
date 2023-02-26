from errors import ServerException


class JWTDecodeException(ServerException):
    """Exception raised when decoding JWT failed"""
