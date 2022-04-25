"""TODO generate docstring"""


from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from bitrender.errors.http import ErrorCode, ErrorModel
from bitrender.errors.user import BadCredentials, NoDefaultRole, UserAlreadyExist, UserNotVerified
from bitrender.models.user import User
from bitrender.schemas import UserCreate, UserSchema
from bitrender.services import user as UserService

router = APIRouter(tags=["auth"])


register_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.NO_DEFAULT_ROLE: {
                        "summary": """Cannot assign role to user.
                            No default role exists in the database.""",
                        "value": {"detail": ErrorCode.NO_DEFAULT_ROLE},
                    },
                    ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS},
                    },
                }
            }
        },
    },
}

login_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Bad credentials or the user is inactive.",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                    },
                    ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                        "summary": "A user with this email already exists.",
                        "value": {"detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS},
                    },
                }
            }
        },
    },
}


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    responses=register_responses,
)
async def register(data: UserCreate):
    try:
        return await UserService.register(data)
    except NoDefaultRole as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.NO_DEFAULT_ROLE,
        ) from error
    except UserAlreadyExist as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        ) from error


@router.post("/login", responses=login_responses)
async def login(response: Response, credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await UserService.authenticate(credentials)
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
    response.delete_cookie("access_token")


@router.post("/request-verify-token")
async def request_verify_token(email: EmailStr):
    pass


@router.post("/verify")
async def verify(email: str):
    user = await User.get_by_email(email)
    user.is_verified = True
    await user.save()


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    pass


@router.post("/reset-password")
async def reset_password(token: str, password: str):
    pass
