from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from bitrender.auth.acl import AclAction, AclList, AclPermit
from bitrender.auth.acl_helper import AclHelper
from tests.unit.models import ExampleModel


def test_sacl_simple_success(mocker: MockerFixture):
    """Tests the get_latest method with lock set to False."""
    acl_action = AclAction.CREATE
    model_sacl: AclList = [(AclPermit.ALLOW, "user:test", AclAction.CREATE)]
    user_acl_ids = [("user:test")]
    __test_sacl(user_acl_ids, model_sacl, mocker, acl_action, True)


def __test_sacl(
    auth_ids: list[str], sacl: AclList, mocker: MockerFixture, action: AclAction, result: bool
):
    mock_sacl = MagicMock(return_value=sacl)
    mocker.patch("tests.unit.models.ExampleModel.__sacl__", new=mock_sacl)
    acl_helper = AclHelper(auth_ids)
    assert acl_helper.static_check([ExampleModel], action) == result


def __mock_sacl(sacl: AclList):
    mock = MagicMock(return_value=sacl)


async def test_sacl_multiple_models_success():
    pass


async def test_sacl_multiple_actions_failure():
    pass


async def __test_acl_helper(auth_ids: list[str], sacl: AclList, dacl: list[AclList]):
    acl_helper = AclHelper(auth_ids)
