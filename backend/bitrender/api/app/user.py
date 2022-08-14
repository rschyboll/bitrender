"""Contains frontend router definition."""
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from bitrender.api.app.responses.user import (
    user_by_id_responses,
    user_logged_responses,
    user_login_responses,
    user_me_responses,
    user_register_responses,
)
from bitrender.api.deps.user import UserContext, get_current_user
from bitrender.api.inject import InjectInRoute
from bitrender.schemas import UserView
from bitrender.schemas.user import UserCreate
from bitrender.services.app import IUserService

user_router = APIRouter(prefix="/user", responses=user_me_responses)


@user_router.post("/login", responses=user_login_responses)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> None:
    """
    Authenticates a user, and stores his web token as a http only cookie.
    To login, the user needs to provide the following data:

    - **username/email**: unique email or username of that user
    - **password**: password of that user

    When the user could not be authenticated for one of the following reasons:
    - the user was not found in the database
    - the password for that user was wrong
    - the user is not active

    The server responds with a 401 status code and a BAD_CREDENTIALS error code.

    When the user is not yet verified, the server responds with a 401 status code and a \
        USER_NOT_VERIFIED error code.
    """
    token = await user_service.authenticate(credentials.username, credentials.password)
    response.set_cookie(
        "access_token",
        f"Bearer {token}",
        secure=True,
        httponly=True,
        samesite="None",
        expires=60 * 60 * 24,
    )


@user_router.post("/register", responses=user_register_responses)
async def register(
    user_data: UserCreate,
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> None:
    """
    Creates a new user, with the default role that is currently selected in the system.
    To register a new user, the following data needs to be provided:

    - **email**: a unique email for the new user
    - **password**: password for the new user

    When a user with the provided email already exists, the server responds with a 409 status, \
        and a EMAIL_TAKEN error code.

    When a user with the provided username already exists, the server responds with a 409 status, \
        and a USERNAME_TAKEN error code.

    When no default role is selected in the system, the server responds with a 503 status, \
        and a NO_DEFAULT_ROLE error code.

    The password and email fields are beeing verified. If they do not met the following rules:
    - the password needs to be 10 characters long, and contain one number, one lowercase and one \
        uppercase character
    - the email needs to fulfill the requirements from the \
        [python-email-validation](https://github.com/JoshData/python-email-validator) library

    The server responds with a 422 status code, and details generated by pydantic validation error.
    """
    await user_service.register(user_data)


@user_router.get(
    "/me",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_logged_responses,
)
async def get_me(
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    """
    Returns the data (name, email, role, permissions etc.) of the current authenticated user.
    This route could be used as a check on app startup, to check if the user is logged in.

    Returns an instance of the UserView schema.
    When no user is currently authenticated, the server responds with a 401 status code, \
        and a NOT_AUTHENTICATED error code.

    When the user has no access to it's data (which suggests some kind of server bug), \
        the server responds with a 401 status code and a NOT_AUTHORIZED error code.
    """
    return await user_service.get_current()


@user_router.get(
    "/logged",
    responses=user_me_responses,
)
async def logged(
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> bool:
    """Returns a boolean, that shows if there is an user current authenticated.

    Can be used, to check the authentication, without the need to check the http status code.
    Useful when there are autmatic mechanisms that listen for the 401 status code, and a \
        NOT_AUTHENTICATED error code.
    """
    return await user_service.logged()


@user_router.get("/request-validation")
async def request_validation(
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    pass


@user_router.post("/validate")
async def validate(
    token: str,
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    pass


@user_router.post("/validate/{token}")
async def validate_with_key(
    token: str,
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    pass


@user_router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserView,
    responses=user_by_id_responses,
)
async def get_by_id(
    user_id: UUID,
    user_service: IUserService = Depends(InjectInRoute(IUserService, UserContext, "context")),
) -> UserView:
    return await user_service.get_by_id(user_id)