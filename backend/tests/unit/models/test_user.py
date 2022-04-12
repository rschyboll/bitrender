"""TODO generate docstring"""
import random
import string

from tortoise.contrib.test import TruncationTestCase

from bitrender.models import User


class TestUser(TruncationTestCase):
    """TODO generate docstring"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_models: list[User] = []

    async def asyncSetUp(self):
        """Creates user entries used in other tests"""
        await super().asyncSetUp()

    @staticmethod
    def __string_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))
