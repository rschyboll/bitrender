from errors import UserError


class ConnectionException(UserError):
    pass


class WrongResponseException(UserError):
    pass
