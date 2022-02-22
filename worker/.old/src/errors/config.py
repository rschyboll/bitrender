from errors import UserError


class SettingsWriteError(UserError):
    pass


class SettingsReadError(UserError):
    pass


class SettingsNotReadError(UserError):
    pass
