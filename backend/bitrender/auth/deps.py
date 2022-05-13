"""TODO generate docstring"""
from fastapi import Depends
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from bitrender.auth.acl import AUTHENTICATED, EVERYONE, SUPERUSER
from bitrender.auth.jwt import TokenHelper
from bitrender.auth.transport import OAuth2PasswordBearerWithCookie
from bitrender.errors.auth import TokenError, UnauthorizedError
from bitrender.models import User

oauth2_scheme = OAuth2PasswordBearerWithCookie("/login", False)


async def get_current_user(token: str | None = Depends(oauth2_scheme)) -> User:
    """Extracts user data from the JWT, validates it and returns the current user.
    Returns None, if the token is expired, is corrupted, or when the user does not exist.

    Args:
        token (str | None, optional): JWT token extracted from Request headers.\
            Defaults to Depends(oauth2_scheme).

    Returns:
        User | None: Current user, or None, if no user could be authenticated."""
    token_helper = TokenHelper()
    if token is None:
        raise UnauthorizedError()
    try:
        token_data = token_helper.decode_token(token)
        user = await User.get_by_id(token_data.sub, False)
        return user
    except (TokenError, ValidationError, DoesNotExist) as error:
        raise UnauthorizedError() from error


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
    except (TokenError, ValidationError, DoesNotExist):
        return None


async def get_auth_ids(user: User | None = Depends(get_current_user_or_none)) -> list[str]:
    """TODO generate docstring."""
    if user is None or not user.is_active or not user.is_verified:
        return [EVERYONE]
    if user.is_superuser:
        return [*(await user.acl_id_list), SUPERUSER, AUTHENTICATED, EVERYONE]
    return [*(await user.acl_id_list), AUTHENTICATED, EVERYONE]
