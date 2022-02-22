from .base import BaseCreate, BaseView


class BinaryView(BaseView):
    version: str
    url: str


class BinaryCreate(BaseCreate):
    version: str
    url: str
