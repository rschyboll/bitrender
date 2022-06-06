"""TODO generate docstring"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from bitrender.api.responses import ErrorCode
from bitrender.api.responses.auth import login_responses, register_responses
from bitrender.errors.auth import BadCredentials, NoDefaultRole, UserNotVerified
from bitrender.errors.user import UserAlreadyExists
from bitrender.models.user import User
from bitrender.schemas import UserCreate, UserSchema
from bitrender.services import Services

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    responses=register_responses,
)
async def register(user_data: UserCreate, services: Services = Depends()) -> User:
    """Registers a new user in the system."""
    try:
        return await services.auth.register(user_data)
    except NoDefaultRole as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.NO_DEFAULT_ROLE,
        ) from error
    except UserAlreadyExists as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        ) from error


@router.post("/login", responses=login_responses)
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    services: Services = Depends(),
):
    """TODO generate docstring"""
    try:
        token = await services.auth.authenticate(credentials)
        response.set_cookie("access_token", f"Bearer {token}", httponly=True)
    except BadCredentials as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        ) from error
    except UserNotVerified as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
        ) from error


@router.post("/logout")
async def logout(response: Response):
    """TODO generate docstring"""
    response.delete_cookie("access_token")


@router.post("/request-verify-token")
async def request_verify_token(email: EmailStr, services: Services = Depends()):
    await services.auth.request_verify(email)


@router.post("/verify")
async def verify(email: EmailStr, token: str, services: Services = Depends()):
    await services.auth.verify(email, token)


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    pass


@router.post("/reset-password")
async def reset_password(token: str, password: str):
    pass
