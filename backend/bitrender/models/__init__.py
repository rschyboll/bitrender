from .role import Role
from .user import User


def register_db(app: FastAPI) -> None:
    config = get_tortoise_config()
    register_tortoise(app, config=config, add_exception_handlers=True)
