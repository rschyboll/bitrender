"""Contains tests for the AclHelper class from bitrender.auth.acl_helper"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_mock import MockerFixture

from bitrender.core.acl import AUTHENTICATED, EVERYONE, AclAction, AclEntry, AclList, AclPermit
from bitrender.services.helpers.core.acl import AclHelper
from tests.utils.models import ExampleModel

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
    """Tests if checks respond correctly to given permits."""
    auth_id = "user:test"
    action = AclAction.CREATE
    acl: AclList = [(permit, auth_id, action)]
    assert __static_check(action, acl, [auth_id] if has_auth_id else []) == result
    assert await __dynamic_check(action, [acl], [auth_id] if has_auth_id else []) == result


test_actions_parameters = [
    (AclAction.CREATE, (AclPermit.DENY, AUTHENTICATED, AclAction.CREATE), False),
    (AclAction.CREATE, (AclPermit.DENY, AUTHENTICATED, AclAction.VIEW), None),
    (AclAction.VIEW, (AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW), True),
    (AclAction.VIEW, (AclPermit.ALLOW, AUTHENTICATED, AclAction.CREATE), None),
]


@pytest.mark.parametrize("action,acl_entry,result", test_actions_parameters)
async def test_actions(
    action: AclAction, acl_entry: AclEntry | list[AclEntry], result: bool | None
):
    """Tests checks responding only to required actions."""
    if not isinstance(acl_entry, list):
        acl_entry = [acl_entry]
    assert __static_check(action, acl_entry, [AUTHENTICATED]) == result
    assert await __dynamic_check(action, [acl_entry], [AUTHENTICATED]) == result


test_acl_order_parameters = [
    (
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.DENY, AUTHENTICATED, AclAction.DELETE),
        ],
        True,
    ),
    (
        [
            (AclPermit.DENY, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
        ],
        False,
    ),
]


@pytest.mark.parametrize("acl_list,result", test_acl_order_parameters)
async def test_acl_order(acl_list: AclList, result: bool | None):
    """Tests if the order of acl_entries is respected."""
    assert __static_check(AclAction.DELETE, acl_list, [AUTHENTICATED]) == result
    assert await __dynamic_check(AclAction.DELETE, [acl_list], [AUTHENTICATED]) == result


test_multiple_required_actions_parameters = [
    (
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.CREATE),
        ],
        [AclAction.DELETE, AclAction.CREATE],
        True,
    ),
    (
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.DENY, AUTHENTICATED, AclAction.CREATE),
        ],
        [AclAction.DELETE, AclAction.CREATE],
        False,
    ),
    (
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.ALLOW, "Test", AclAction.CREATE),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW),
        ],
        [AclAction.DELETE, AclAction.CREATE, AclAction.VIEW],
        None,
    ),
    (
        [
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
            (AclPermit.NOTALLOW, "Test", AclAction.CREATE),
            (AclPermit.ALLOW, AUTHENTICATED, AclAction.VIEW),
        ],
        [AclAction.DELETE, AclAction.CREATE, AclAction.VIEW],
        True,
    ),
]


@pytest.mark.parametrize("acl_list,actions,result", test_multiple_required_actions_parameters)
async def test_multiple_required_actions(
    acl_list: AclList, actions: list[AclAction], result: bool | None
):
    """Tests correctly checking if multiple actions are required"""
    assert __static_check(actions, acl_list, [AUTHENTICATED]) == result
    assert await __dynamic_check(actions, [acl_list], [AUTHENTICATED]) == result


test_multiple_auth_ids_parameters = [
    (
        [AUTHENTICATED, "user:123", "permission:123"],
        (AclPermit.DENY, AUTHENTICATED, AclAction.DELETE),
        AclAction.DELETE,
        False,
    ),
    (
        [AUTHENTICATED, "user:123", "permission:123"],
        (AclPermit.ALLOW, AUTHENTICATED, AclAction.DELETE),
        AclAction.DELETE,
        True,
    ),
]


@pytest.mark.parametrize("auth_ids,acl_entry,action,result", test_multiple_auth_ids_parameters)
async def test_multiple_auth_ids(
    auth_ids: list[str], acl_entry: AclEntry, action: AclAction, result: bool | None
):
    """Tests correctly checking if multiple acl_entries are provided"""
    assert __static_check([action], [acl_entry], auth_ids) == result
    assert await __dynamic_check([action], [[acl_entry]], auth_ids) == result


test_multiple_required_auth_ids_parameters = [
    (
        [AUTHENTICATED, "user:123", "permission:123"],
        (AclPermit.DENY, [AUTHENTICATED, "user:123"], AclAction.DELETE),
        AclAction.DELETE,
        False,
    ),
    (
        [AUTHENTICATED, "user:123", "permission:123"],
        (AclPermit.ALLOW, [AUTHENTICATED, "user:123"], AclAction.DELETE),
        AclAction.DELETE,
        True,
    ),
]


@pytest.mark.parametrize(
    "auth_ids,acl_entry,action,result", test_multiple_required_auth_ids_parameters
)
async def test_multiple_required_auth_ids(
    auth_ids: list[str], acl_entry: AclEntry, action: AclAction, result: bool | None
):
    """Tests correctly checking if multiple acl_entries are provided"""
    assert __static_check([action], [acl_entry], auth_ids) == result
    assert await __dynamic_check([action], [[acl_entry]], auth_ids) == result


test_multiple_actions_in_entry_parameters = [
    (
        AUTHENTICATED,
        (AclPermit.DENY, AUTHENTICATED, [AclAction.DELETE, AclAction.VIEW]),
        AclAction.DELETE,
        False,
    ),
    (
        AUTHENTICATED,
        (AclPermit.ALLOW, AUTHENTICATED, [AclAction.DELETE, AclAction.VIEW]),
        AclAction.EDIT,
        None,
    ),
]


@pytest.mark.parametrize(
    "auth_id,acl_entry,action,result", test_multiple_actions_in_entry_parameters
)
async def test_multiple_actions_in_entry(
    auth_id: str, acl_entry: AclEntry, action: AclAction, result: bool | None
):
    """Tests correctly checking if multiple actions are in one AclEntry"""
    assert __static_check([action], [acl_entry], [auth_id]) == result
    assert await __dynamic_check([action], [[acl_entry]], [auth_id]) == result


async def test_dynamic_multiple_resources():
    """Tests correctly checking if multiple resources are provided to dynamic"""
    assert await __dynamic_check_multiple_resources(
        AclAction.CREATE,
        [[(AclPermit.ALLOW, AUTHENTICATED, AclAction.CREATE)]],
        [AUTHENTICATED],
    )
    assert not (
        await __dynamic_check_multiple_resources(
            AclAction.CREATE,
            [[(AclPermit.DENY, AUTHENTICATED, AclAction.CREATE)]],
            [AUTHENTICATED],
        )
    )


def __static_check(actions: list[AclAction] | AclAction, sacl: AclList, auth_ids: list[str]):
    with patch("tests.utils.models.ExampleModel.__sacl__", new=MagicMock(return_value=sacl)):
        acl_helper = AclHelper()
        return acl_helper.static([ExampleModel], actions, auth_ids)


async def __dynamic_check(
    actions: list[AclAction] | AclAction, dacl: list[AclList], auth_ids: list[str]
):
    with patch("tests.utils.models.ExampleModel.__dacl__", new=AsyncMock(return_value=dacl)):
        acl_helper = AclHelper()
        model = ExampleModel()
        return await acl_helper.dynamic(model, actions, auth_ids)


async def __dynamic_check_multiple_resources(
    actions: list[AclAction] | AclAction, dacl: list[AclList], auth_ids: list[str]
):
    with patch("tests.utils.models.ExampleModel.__dacl__", new=AsyncMock(return_value=dacl)):
        acl_helper = AclHelper()

        return await acl_helper.dynamic(
            [ExampleModel(), ExampleModel(), ExampleModel(), ExampleModel()], actions, auth_ids
        )
