"""This module contains tests for Subprocess class from bitrender_worker.utils.subprocess."""
from typing import List
from unittest.mock import AsyncMock, call

import pytest
from pytest_mock import MockerFixture

from bitrender_worker.utils.subprocess import MessageSource, Subprocess
from tests.mocks.subprocess import MockProcess, mock_create_subprocess_exec


@pytest.mark.asyncio
async def test_return_code(mocker: MockerFixture):
    """Tests returning correnct returncode from run method."""
    for returncode in range(0, 255):
        process_mock = MockProcess(returncode)
        mock_create_subprocess_exec(mocker, process_mock)

        subprocess = Subprocess("", [], AsyncMock())
        assert returncode == await subprocess.run()


@pytest.mark.asyncio
@pytest.mark.parametrize("stdout", [[], [b"1"], [b"234", b"567", b"890", b"123"]])
@pytest.mark.parametrize("stderr", [[], [b"4"], [b"567", b"890", b"123", b"456"]])
async def test_on_message_callback(mocker: MockerFixture, stdout: List[bytes], stderr: List[bytes]):
    """Tests correct calling the on_message callback."""

    expected_calls = [
        *[call({"text": arg.decode(), "source": MessageSource.STDOUT}) for arg in stdout],
        *[call({"text": arg.decode(), "source": MessageSource.STDERR}) for arg in stderr],
    ]

    process_mock = MockProcess(0, stdout, stderr)
    mock_create_subprocess_exec(mocker, process_mock)

    on_message_mock = AsyncMock()
    subprocess = Subprocess("", [], on_message_mock)

    await subprocess.run()

    assert on_message_mock.call_count == len(expected_calls)
    for expected_call in expected_calls:
        assert expected_call in on_message_mock.call_args_list


async def test_message_not_decodable(mocker: MockerFixture):
    pass


async def test_stop_process(mocker: MockerFixture):
    process_mock = MockProcess(timeout=1000)
    mock_create_subprocess_exec(mocker, process_mock)
    