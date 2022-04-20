from bitrender.models import Permission, Role, User


async def generate_permissions() -> list[Permission]:
    pass


async def generate_roles() -> list[Role]:
    pass


async def generate_users(
    amount: int,
    username_prefix: str,
    email_prefix: str,
    role: Role,
    active: bool = False,
) -> list[User]:
    """TODO generate docstring"""
    users: list[User] = []
    for i in range(0, amount):
        username = f"{username_prefix}_{str(i)}"
        email = f"{email_prefix}_{str(i)}"
        user = User(username=username, email=email, role=role, active=active)
        await user.save()
        users.append(user)
    return users
