from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from bitrender.auth.jwt import decode_token, jwt
from bitrender.models import User


class CredentialsException(HTTPException):
    """TODO generate costring"""

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Not authenticated",
        headers: dict[str, Any] | None = None,
    ) -> None:
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class OAuth2PasswordBearerWithCookie(OAuth2):
    """TODO generate docstring"""

    def __init__(self, tokenUrl: str, auto_error: bool = True):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")
        if authorization is None:
            raise CredentialsException()

        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise CredentialsException()
            return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie("/login", False)


async def get_current_user_or_none(token: str | None = Depends(oauth2_scheme)) -> User | None:
    """Extracts user data from the JWT, validates it and returns the current user.
    Returns None, if the token is expired, is corrupted, or when the user does not exist.

    Args:
        token (str | None, optional): JWT token extracted from Request headers.\
            Defaults to Depends(oauth2_scheme).

    Returns:
        User | None: Current user, or None, if no user could be authenticated."""
    if token is None:
        return None
    try:
        token_data = decode_token(token)
        user = await User.get_by_id(token_data.sub, False)
        return user
    except (jwt.JWTError, ValidationError, DoesNotExist):
        return None


async def get_active_user(user: User | None = Depends(get_current_user_or_none)) -> User:
    """_summary_

    Args:
        user (User | None, optional): _description_. Defaults to Depends(get_current_user_or_none).

    Raises:
        HTTPException: _description_

    Returns:
        User: _description_
    """
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
