from typing import Optional


class UserException(Exception):
    message: Optional[str]

    def __init__(self, context: Optional[str] = None):
        super(UserException, self).__init__()
        self.context = context
