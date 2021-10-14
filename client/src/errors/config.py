from errors import UserError


class SettingsWriteError(UserError):
    message = "Can't save settings. Check permissions of app data folder."


class SettingsReadError(UserError):
    message = "Can't read settings, if you are not registered, try removing "


class SettingsNotReadError(UserError):
    pass
