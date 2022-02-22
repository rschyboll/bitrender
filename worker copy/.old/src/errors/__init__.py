from typing import Optional


class UserError(Exception):
    message: Optional[str] = None

    def __init__(self, context: Optional[str] = None):
        super(UserError, self).__init__()
        self.context = context
