from abc import ABC, abstractmethod
from uuid import UUID

from bitrender.models import Role
from bitrender.schemas import UserCreate


class IUserService(ABC):
    @abstractmethod
    def create(self, data: UserCreate, role: Role | UUID):
        ...
