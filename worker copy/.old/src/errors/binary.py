from errors import UserError


class BinaryVersionCheckError(UserError):
    message = """Can't check for new Blender binary version.
Check if any binaries were added to the server"""


class OSSaveError(UserError):
    message = """Can't write to apps data dir. Check permissions."""
