from fastapi import BackgroundTasks, Depends

from bitrender.auth.acl_helper import AclHelper
from bitrender.auth.deps import get_auth_ids
from bitrender.auth.jwt import TokenHelper
from bitrender.auth.password import PasswordHelper
from bitrender.config import Settings, get_settings
from bitrender.services.auth import AuthService
from bitrender.services.email import EmailService


class Services:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        auth_ids: list[str] = Depends(get_auth_ids),
        settings: Settings = Depends(get_settings),
    ):
        password_helper = PasswordHelper()
        self.background_tasks = background_tasks
        self.settings = settings
        self.auth = AuthService(self, password_helper, TokenHelper(), AclHelper(auth_ids))
        self.email = EmailService(self, settings)
