"""TODO generate docstring"""
from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from bitrender.auth.jwt import TokenHelper
from bitrender.core.acl import AUTHENTICATED, EVERYONE, SUPERUSER
from bitrender.errors.auth import TokenCorruptedError, TokenExpiredError, UnauthenticatedError
from bitrender.models import User


class OAuth2PasswordBearerWithCookie(OAuth2):
    """TODO generate docstring"""

    def __init__(self, tokenUrl: str, auto_error: bool = True):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")
        if authorization is None:
            if self.auto_error:
                raise UnauthenticatedError()
            return None
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthenticatedError()
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
    token_helper = TokenHelper()
    if token is None:
        return None
    try:
        token_data = token_helper.decode_token(token)
        user = await User.get_by_id(token_data.sub, False)
        return user
    except (TokenCorruptedError, TokenExpiredError, ValidationError, DoesNotExist):
        return None


async def get_current_user(user: User | None = Depends(get_current_user_or_none)) -> User:
    """Returns the current user from the request, and raises an error if no current user could be\
         authenticated.

    Args:
        user (User | None, optional): Current user or none. \
            Defaults to Depends(get_current_user_or_none).

    Raises:
        UnauthenticatedError: Raised if no user could be authenticated.

    Returns:
        User: The current user.
    """
    if user is None:
        raise UnauthenticatedError()
    return user


async def get_auth_ids(user: User | None = Depends(get_current_user_or_none)) -> list[str]:
    """TODO generate docstring."""
    if user is None or not user.is_active or not user.is_verified:
        return [EVERYONE]
    if user.is_superuser:
        return [*(await user.acl_id_list), SUPERUSER, AUTHENTICATED, EVERYONE]
    return [*(await user.acl_id_list), AUTHENTICATED, EVERYONE]
