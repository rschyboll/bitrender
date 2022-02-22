"""This module contains tests for Subprocess class from bitrender_worker.utils.subprocess."""
import asyncio
from typing import List, Tuple
from unittest.mock import AsyncMock, _Call, call

import pytest

from bitrender_worker.utils.subprocess import Subprocess
from tests.mocks.subprocess import MockProcess, MockStreamReader


@pytest.mark.asyncio
async def test_return_code(process: MockProcess):
    """Tests returning correct returncode from run method."""
    for returncode in range(-255, 255):
        subprocess = Subprocess("", [], AsyncMock(), AsyncMock())

        process.returncode = returncode
        assert subprocess.returncode is None
        run_returncode = await subprocess.run()
        assert returncode == run_returncode
        assert returncode == subprocess.returncode


@pytest.mark.asyncio
@pytest.mark.parametrize("stdout", [[], [b"1"], [b"234", b"567", b"890", b"123"]])
@pytest.mark.parametrize("stderr", [[], [b"4"], [b"567", b"890", b"123", b"456"]])
async def test_on_message_callback(process: MockProcess, stdout: List[bytes], stderr: List[bytes]):
    """Tests correct calling the on_message callback."""
    on_stdout_mock, on_stderr_mock = AsyncMock(), AsyncMock()

    subprocess = Subprocess("", [], on_stdout_mock, on_stderr_mock)

    process.stdout = MockStreamReader(stdout.copy())
    process.stderr = MockStreamReader(stderr.copy())

    await subprocess.run()

    __assert_correct_calls(on_stdout_mock, on_stderr_mock, stdout, stderr)


def __generate_calls(stdout: List[bytes], stderr: List[bytes]) -> Tuple[List[_Call], List[_Call]]:
    return (
        [call(message.decode()) for message in stdout],
        [call(message.decode()) for message in stderr],
    )


def __assert_correct_calls(
    on_stdout_mock: AsyncMock, on_stderr_mock: AsyncMock, stdout: List[bytes], stderr: List[bytes]
) -> None:
    stdout_calls, stderr_calls = __generate_calls(stdout, stderr)
    assert on_stdout_mock.call_count == len(stdout_calls)
    assert on_stderr_mock.call_count == len(stderr_calls)
    for expected_call in stdout_calls:
        assert expected_call in on_stdout_mock.call_args_list
    for expected_call in stderr_calls:
        assert expected_call in on_stderr_mock.call_args_list


@pytest.mark.asyncio
async def test_stop(process: MockProcess):
    """Tests correct subprocess terminating when calling the stop method."""
    subprocess = Subprocess("", [], AsyncMock(), AsyncMock())

    process.wait_for_terminate = True

    run_task = asyncio.create_task(subprocess.run())
    await asyncio.sleep(0.00001)

    assert subprocess.returncode is None
    await subprocess.stop()
    assert subprocess.returncode is None

    process.returncode = -1

    assert await run_task == -1
    process.terminate.assert_called()


@pytest.mark.asyncio
async def test_stop_not_running(process: MockProcess):
    """Tests calling stop on Subprocess without launching it."""
    on_stdout_mock, on_stderr_mock = AsyncMock(), AsyncMock()
    subprocess = Subprocess("", [], on_stdout_mock, on_stderr_mock)

    await subprocess.stop()
    process.terminate.assert_not_called()


@pytest.mark.asyncio
async def test_wrong_messages(process: MockProcess):
    """Tests correct calling the on_message callback."""
    on_stdout_mock, on_stderr_mock = AsyncMock(), AsyncMock()
    subprocess = Subprocess("", [], on_stdout_mock, on_stderr_mock)

    process.stdout = MockStreamReader([b"\xed"])
    process.stderr = MockStreamReader([b"\xea"])

    await subprocess.run()

    assert on_stdout_mock.call_count == 0
    assert on_stderr_mock.call_count == 0
