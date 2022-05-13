"""TODO generate docstring"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from bitrender.auth.acl import AUTHENTICATED, EVERYONE, AclAction, AclList, AclPermit
from bitrender.auth.acl_helper import AclHelper
from tests.unit.models import ExampleModel

test_permits_parameters = [
    (AclPermit.ALLOW, True, True),
    (AclPermit.ALLOW, False, None),
    (AclPermit.DENY, True, False),
    (AclPermit.DENY, False, None),
    (AclPermit.NOTALLOW, True, None),
    (AclPermit.NOTALLOW, False, True),
    (AclPermit.NOTDENY, True, None),
    (AclPermit.NOTDENY, False, False),
]


@pytest.mark.parametrize("permit,has_auth_id,result", test_permits_parameters)
async def test_permits(permit: AclPermit, has_auth_id: bool, result: bool | None):
    """TODO generate docstring"""
    auth_id = "user:test"
    action = AclAction.CREATE
    acl: AclList = [(permit, auth_id, action)]
    assert __static_check(action, acl, [auth_id] if has_auth_id else []) == result
    assert await __dynamic_check(action, [acl], [auth_id] if has_auth_id else []) == result


async def test_acl_order():
    pass


async def test_multiple_entries():
    pass


async def test_multiple_actions():
    pass


def __static_check(actions: list[AclAction] | AclAction, sacl: AclList, auth_ids: list[str]):
    with patch("tests.unit.models.ExampleModel.__sacl__", new=MagicMock(return_value=sacl)):
        acl_helper = AclHelper(auth_ids)
        return acl_helper.static_check([ExampleModel], actions)


async def __dynamic_check(
    actions: list[AclAction] | AclAction, dacl: list[AclList], auth_ids: list[str]
):
    with patch("tests.unit.models.ExampleModel.__dacl__", new=AsyncMock(return_value=dacl)):
        acl_helper = AclHelper(auth_ids)
        model = ExampleModel()
        return await acl_helper.dynamic_check(model, actions)


sacl_simple_allow_parameters = [
    (AclAction.CREATE, [(AclPermit.ALLOW, "user:123", AclAction.CREATE)], ["user:123"]),
    (AclAction.VIEW, [(AclPermit.ALLOW, EVERYONE, AclAction.VIEW)], [EVERYONE]),
    (AclAction.DELETE, [(AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE)], [AUTHENTICATED]),
    (AclAction.EDIT, [(AclPermit.ALLOW, AUTHENTICATED, AclAction.EDIT)], [AUTHENTICATED]),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_simple_allow_parameters)
def test_sacl_simple_allow(
    action: AclAction,
    sacl: AclList,
    auth_ids: list[str],
    result: bool,
    mocker: MockerFixture,
):
    """Tests the get_latest method with lock set to False."""
    __test_sacl(action, sacl, auth_ids, mocker, True)


sacl_simple_deny_parameters = [
    (AclAction.CREATE, [(AclPermit.DENY, "user:123", AclAction.CREATE)], ["user:123"]),
    (AclAction.VIEW, [(AclPermit.DENY, EVERYONE, AclAction.VIEW)], [EVERYONE]),
    (AclAction.DELETE, [(AclPermit.DENY, AUTHENTICATED, AclAction.DELETE)], [AUTHENTICATED]),
    (AclAction.EDIT, [(AclPermit.DENY, AUTHENTICATED, AclAction.EDIT)], [AUTHENTICATED]),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_simple_deny_parameters)
def test_sacl_simple_deny(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """Tests the get_latest method with lock set to False."""
    __test_sacl(action, sacl, auth_ids, mocker, False)


sacl_simple_none_parameters = [
    (AclAction.CREATE, [(AclPermit.ALLOW, "user:321", AclAction.CREATE)], ["user:123"]),
    (AclAction.VIEW, [(AclPermit.DENY, "user:321", AclAction.VIEW)], [EVERYONE]),
    (AclAction.DELETE, [(AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW)], [AUTHENTICATED]),
    (AclAction.EDIT, [(AclPermit.DENY, "user:321", AclAction.DELETE)], [AUTHENTICATED]),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_simple_none_parameters)
def test_sacl_simple_none(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """Tests the get_latest method with lock set to False."""
    __test_sacl(action, sacl, auth_ids, mocker, None)


sacl_simple_not_deny_parameters = [
    (AclAction.CREATE, [(AclPermit.NOTDENY, "user:321", AclAction.CREATE)], ["user:123"]),
    (AclAction.VIEW, [(AclPermit.NOTDENY, "user:123", AclAction.VIEW)], [EVERYONE]),
    (AclAction.DELETE, [(AclPermit.NOTDENY, EVERYONE, AclAction.DELETE)], [AUTHENTICATED]),
    (AclAction.VIEW, [(AclPermit.NOTDENY, EVERYONE, AclAction.VIEW)], [AUTHENTICATED]),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_simple_not_deny_parameters)
def test_sacl_simple_not_deny(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """Tests the get_latest method with lock set to False."""
    __test_sacl(action, sacl, auth_ids, mocker, False)


sacl_simple_not_allow_parameters = [
    (AclAction.CREATE, [(AclPermit.NOTALLOW, "user:321", AclAction.CREATE)], ["user:123"]),
    (AclAction.VIEW, [(AclPermit.NOTALLOW, "user:123", AclAction.VIEW)], [EVERYONE]),
    (AclAction.DELETE, [(AclPermit.NOTALLOW, EVERYONE, AclAction.DELETE)], [AUTHENTICATED]),
    (AclAction.VIEW, [(AclPermit.NOTALLOW, EVERYONE, AclAction.VIEW)], [AUTHENTICATED]),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_simple_not_allow_parameters)
def test_sacl_simple_not_allow(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """Tests the get_latest method with lock set to False."""
    __test_sacl(action, sacl, auth_ids, mocker, True)


sacl_multiple_auth_ids_parameters = [
    (
        AclAction.EDIT,
        [(AclPermit.ALLOW, AUTHENTICATED, AclAction.EDIT)],
        ["user:123", AUTHENTICATED, EVERYONE],
        True,
    ),
    (
        AclAction.CREATE,
        [(AclPermit.ALLOW, "user:432", AclAction.CREATE)],
        ["user:432", "user:123", AUTHENTICATED, EVERYONE],
        True,
    ),
]


@pytest.mark.parametrize("action,sacl,auth_ids,result", sacl_multiple_auth_ids_parameters)
def test_sacl_multiple_auth_ids(
    action: AclAction | list[AclAction],
    sacl: AclList,
    auth_ids: list[str],
    result: bool | None,
    mocker: MockerFixture,
):
    """TODO generate docstring"""
    __test_sacl(action, sacl, auth_ids, mocker, result)


sacl_multiple_required_actions_parameters_allow = [
    (
        [AclAction.EDIT, AclAction.CREATE],
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.EDIT),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.CREATE),
        ],
        ["user:123", AUTHENTICATED, EVERYONE],
    ),
    (
        [AclAction.VIEW, AclAction.DELETE],
        [
            (AclPermit.ALLOW, "user:432", AclAction.VIEW),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
        ],
        ["user:432", "user:123", AUTHENTICATED, EVERYONE],
    ),
    (
        [AclAction.VIEW, AclAction.DELETE, AclAction.EDIT, AclAction.CREATE],
        [
            (AclPermit.ALLOW, "user:432", AclAction.VIEW),
            (AclPermit.ALLOW, "user:123", AclAction.DELETE),
            (AclPermit.ALLOW, "user:432", AclAction.EDIT),
            (AclPermit.ALLOW, "user:123", AclAction.CREATE),
        ],
        ["user:432", "user:123"],
    ),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_multiple_required_actions_parameters_allow)
def test_sacl_multiple_required_actions_allow(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """TODO generate docstring"""
    __test_sacl(action, sacl, auth_ids, mocker, True)


sacl_additional_acl_entries_allow_parameters = [
    (
        [AclAction.EDIT],
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW),
            (AclPermit.ALLOW, "user:123", AclAction.EDIT),
            (AclPermit.DENY, "user:456", AclAction.CREATE),
            (AclPermit.DENY, EVERYONE, AclAction.VIEW),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.EDIT),
        ],
        ["user:123", AUTHENTICATED],
    ),
    (
        [AclAction.VIEW],
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW),
            (AclPermit.ALLOW, "user:123", AclAction.VIEW),
            (AclPermit.DENY, "user:456", AclAction.CREATE),
            (AclPermit.DENY, EVERYONE, AclAction.DELETE),
            (AclPermit.DENY, EVERYONE, AclAction.EDIT),
            (AclPermit.DENY, EVERYONE, AclAction.CREATE),
            (AclPermit.ALLOW, EVERYONE, AclAction.VIEW),
        ],
        [EVERYONE],
    ),
]


@pytest.mark.parametrize("action,sacl,auth_ids", sacl_additional_acl_entries_allow_parameters)
def test_sacl_additional_acl_entries_allow(
    action: AclAction | list[AclAction], sacl: AclList, auth_ids: list[str], mocker: MockerFixture
):
    """TODO generate docstring"""
    __test_sacl(action, sacl, auth_ids, mocker, True)


def __test_sacl(
    action: AclAction | list[AclAction],
    sacl: AclList,
    auth_ids: list[str],
    mocker: MockerFixture,
    result: bool | None,
):
    __mock_sacl(sacl, mocker)
    acl_helper = AclHelper(auth_ids)
    assert acl_helper.static_check([ExampleModel], action) == result


def __mock_sacl(sacl: AclList, mocker: MockerFixture):
    mock = MagicMock(return_value=sacl)
    mocker.patch("tests.unit.models.ExampleModel.__sacl__", new=mock)
