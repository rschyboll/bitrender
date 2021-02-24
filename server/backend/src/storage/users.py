"""CRUD utilities for user"""
from models.user import User

async def create(user: User):
    """Creates user in database"""
    await user.save()
