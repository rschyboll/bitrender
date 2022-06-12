from antidote import implements

from bitrender.schemas import UserView
from bitrender.services.user.core import Service
from bitrender.services.user.interfaces.user import IUserService


@implements(IUserService).by_default
class UserService(Service, IUserService):
    async def get_current(self) -> UserView:
        return await self.services.context.current_user.to_view()
