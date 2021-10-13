from errors import UserError


class BinaryDownloadException(UserError):
    error_message = """
        Can't download blender binaries, no saved binary version found.
        {}
    """


class OSSaveError(UserError):
    error_message = """
        Can't save files to file system, check .local/share privileges.
        {}
    """
