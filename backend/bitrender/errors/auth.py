from fastapi import FastAPI

from bitrender.errors.base import AppException


class AuthException(AppException):
    pass


def auth_exception_handler():
    pass


def add_auth_exception_handlers(app: FastAPI):
    pass
