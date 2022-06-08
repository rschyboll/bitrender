"""Contains frontend router definition."""

from fastapi import APIRouter, Depends

from bitrender.services.user import UserServices

frontend_router = APIRouter(prefix="/user")


@frontend_router.get("/me")
async def get_me(services: UserServices = Depends()):
    print(services)
    print(services.current_user)
    print(services.user_service)
    print(services.user_service.services)
