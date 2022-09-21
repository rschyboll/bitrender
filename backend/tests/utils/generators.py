"""Contains methods for generating fake database data."""
import bcrypt
from faker import Faker

from bitrender.enums.permission import Permission
from bitrender.models import Role, RolePermission, User
from tests.utils.models import ExampleModel

fake = Faker()
fake.seed_instance(123)


async def generate_example_models(amount: int) -> list[ExampleModel]:
    """Generates example models for testing.

    Args:
        amount (int): How many models to generate.

    Returns:
        list[ExampleModel]: List with generated models."""
    models: list[ExampleModel] = []
    for i in range(0, amount):
        model = ExampleModel(char_field=fake.unique.name(), int_field=i)
        await model.save()
        models.append(model)
    return models


async def generate_role_permissions(
    role: Role, permissions: list[Permission]
) -> list[RolePermission]:
    """Generates role permissions for testing.

    Args:
        role (Role): Role for which the permissions should be generated
        permissions (list[Permission]): Permissions that should be added to the role

    Returns:
        list[RolePermission]: Generated permission assignments"""
    role_permissions: list[RolePermission] = []
    for permission in permissions:
        role_permission = await RolePermission.create(role=role, permission=permission)
        role_permissions.append(role_permission)
    return role_permissions


async def generate_roles(amount: int) -> list[Role]:
    """Generates a specified amount of roles for testing. Names are randomly generated.

    Args:
        amount (int): Amount of roles to generate

    Returns:
        list[Role]: List of created roles."""
    roles: list[Role] = []
    for _ in range(0, amount):
        name = fake.unique.name()
        role = await Role.create(name=name)
        roles.append(role)
    return roles


async def generate_users(
    amount: int,
    role: Role,
    is_active: bool = True,
    is_validated: bool = False,
) -> list[User]:
    """Generates a specified amount of users for testing.
    Email and password are randomly generated.

    Args:
        amount (int): Amount of users to generate
        role (Role): Role of the users
        is_active (bool): If the user should be active. Defaults to False
        is_validated (bool): If the user should be active. Defaults to False

    Returns:
        list[User]: List of created users."""

    users: list[User] = []
    for _ in range(0, amount):
        email = fake.unique.ascii_free_email()
        hashed_password = bcrypt.hashpw(fake.password().encode(), bcrypt.gensalt(4))
        username = fake.unique.name()
        user = await User.create(
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=role,
            is_active=is_active,
            is_validated=is_validated,
        )
        users.append(user)
    return users
