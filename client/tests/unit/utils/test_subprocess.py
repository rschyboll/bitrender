"""This module contains tests for Subprocess class from bitrender_worker.utils.subprocess."""
import asyncio
from typing import List
from unittest.mock import AsyncMock, call

import pytest
from pytest_mock import MockerFixture

from bitrender_worker.utils.subprocess import MessageSource, Subprocess
from tests.mocks.subprocess import MockProcess, mock_create_subprocess_exec


@pytest.mark.asyncio
async def test_return_code(mocker: MockerFixture):
    """Tests returning correct returncode from run method."""
    for returncode in range(-255, 255):
        process_mock = MockProcess(returncode=returncode)
        mock_create_subprocess_exec(mocker, process_mock)

        subprocess = Subprocess("", [], AsyncMock())
        assert subprocess.returncode is None
        run_returncode = await subprocess.run()
        assert returncode == run_returncode
        assert returncode == subprocess.returncode


@pytest.mark.asyncio
@pytest.mark.parametrize("stdout", [[], [b"1"], [b"234", b"567", b"890", b"123"]])
@pytest.mark.parametrize("stderr", [[], [b"4"], [b"567", b"890", b"123", b"456"]])
async def test_on_message_callback(mocker: MockerFixture, stdout: List[bytes], stderr: List[bytes]):
    """Tests correct calling the on_message callback."""

    expected_calls = [
        *[call({"text": arg.decode(), "source": MessageSource.STDOUT}) for arg in stdout],
        *[call({"text": arg.decode(), "source": MessageSource.STDERR}) for arg in stderr],
    ]

    process_mock = MockProcess(stdout_values=stdout, stderr_values=stderr)
    mock_create_subprocess_exec(mocker, process_mock)

    on_message_mock = AsyncMock()
    subprocess = Subprocess("", [], on_message_mock)

    await subprocess.run()

    assert on_message_mock.call_count == len(expected_calls)
    for expected_call in expected_calls:
        assert expected_call in on_message_mock.call_args_list


@pytest.mark.asyncio
async def test_stop(mocker: MockerFixture):
    """Tests correct subprocess terminating when calling the stop method."""
    process_mock = MockProcess(wait_for_terminate=True)
    mock_create_subprocess_exec(mocker, process_mock)

    on_message_mock = AsyncMock()
    subprocess = Subprocess("", [], on_message_mock)

    run_task = asyncio.create_task(subprocess.run())
    await asyncio.sleep(0.00001)

    await subprocess.stop()

    assert subprocess.returncode is None

    process_mock.returncode = -1

    assert await run_task == -1

    process_mock.terminate.assert_called()


@pytest.mark.asyncio
async def test_stop_not_running(mocker: MockerFixture):
    """Tests calling stop on Subprocess without launching it."""
    process_mock = MockProcess(wait_for_terminate=True)
    mock_create_subprocess_exec(mocker, process_mock)

    on_message_mock = AsyncMock()
    subprocess = Subprocess("", [], on_message_mock)

    await subprocess.stop()
    process_mock.terminate.assert_not_called()


@pytest.mark.asyncio
async def test_wrong_messages(mocker: MockerFixture):
    """Tests correct calling the on_message callback."""
    process_mock = MockProcess(stdout_values=[b"\xed"], stderr_values=[b"\xea"])
    mock_create_subprocess_exec(mocker, process_mock)

    on_message_mock = AsyncMock()
    subprocess = Subprocess("", [], on_message_mock)

    await subprocess.run()

    assert on_message_mock.call_count == 0
