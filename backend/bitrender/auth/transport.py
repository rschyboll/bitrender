"""TODO generate docstring"""
from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from bitrender.errors.auth import UnauthorizedError


class OAuth2PasswordBearerWithCookie(OAuth2):
    """TODO generate docstring"""

    def __init__(self, tokenUrl: str, auto_error: bool = True):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")
        if authorization is None:
            if self.auto_error:
                raise UnauthorizedError()
            return None
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedError()
            return None
        return param
