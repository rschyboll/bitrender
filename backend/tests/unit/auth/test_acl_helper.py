from bitrender.auth.acl import AclList
from bitrender.auth.acl_helper import AclHelper
from bitrender.tests.

async def test_sacl_simple_success():
    """Tests the get_latest method with lock set to False."""
    model_acl = [()]
    model_dacl = [()]
    user_acl_ids = [()]


async def test_sacl_multiple_models_success():
    pass


async def test_sacl_multiple_actions_failure():
    pass


async def __test_acl_helper(auth_ids: list[str], sacl: AclList, dacl: list[AclList]):
    acl_helper = AclHelper(auth_ids)
    
