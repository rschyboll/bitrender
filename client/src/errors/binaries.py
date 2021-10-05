from errors import UserException


class BinaryDownloadException(UserException):
    error_message = """
        Can't download blender binaries, no saved binary version found.
        {}
    """


class OSSaveError(UserException):
    error_message = """
        Can't save files to file system, check .local/share privileges.
        {}
    """
