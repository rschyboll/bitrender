from tortoise.contrib.test import TruncationTestCase

from bitrender.models.role import Role


class TestBaseModel(TruncationTestCase):
    async def test_hello(self) -> None:
        test = await Role.get_all()
        print(test)

    async def test_hello2(self) -> None:
        test = await Role.get_all()
        print(test)
