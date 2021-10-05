from errors import UserException


class SettingsWriteError(UserException):
    pass


class SettingsReadError(UserException):
    pass


class SettingsNotReadError(UserException):
    pass
