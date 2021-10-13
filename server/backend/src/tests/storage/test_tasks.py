# pylint: disable=invalid-overridden-method
import os
from typing import Any, List, Optional, Tuple
from uuid import UUID

import aiofiles
import pytest
from tortoise.contrib.test import TruncationTestCase
from tortoise.exceptions import DoesNotExist

from config import get_settings
from models.tasks import Task
from schemas.tasks import TaskCreate
from storage import tasks
from tests.utils.tasks import init_random_task_data, random_task_data

settings = get_settings()


class TestWithData(TruncationTestCase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TestWithData, self).__init__(*args, **kwargs)
        self.test_data: Optional[List[Tuple[UUID, TaskCreate]]] = None

    async def setUp(self) -> None:
        self.test_data = await init_random_task_data()

    async def test_get_with_data(self) -> None:
        tasks_data = await tasks.get()
        if self.test_data is None:
            raise Exception()
        assert len(tasks_data) == len(self.test_data)
        for i, task in enumerate(tasks_data):
            test_id, test_task = self.test_data[i]
            assert task.samples == test_task.samples
            assert task.name == test_task.file.filename
            assert task.id == test_id
            assert task.engine == test_task.engine

    async def test_get_by_id(self) -> None:
        if self.test_data is None:
            raise Exception()
        for test_id, test_task in self.test_data:
            task = await tasks.get_by_id(test_id)
            assert task is not None
            assert task.id == test_id
            assert task.name == test_task.file.filename
            assert task.samples == test_task.samples
            assert task.engine == test_task.engine

    async def test_delete(self) -> None:
        if self.test_data is None:
            raise Exception()
        for test_id, _ in self.test_data:
            await Task.get(id=test_id)
            await tasks.delete(test_id)
            with pytest.raises(DoesNotExist):
                await Task.get(id=test_id)


class TestWithoutData(TruncationTestCase):
    async def test_create_success(self) -> None:
        for _ in range(0, 10):
            task = random_task_data()
            file_bytes = await task.file.read()
            task.file.file.seek(0)
            task_view = await tasks.create(task)

            assert task_view.name == task.file.filename
            assert task_view.engine == task.engine
            assert task_view.id is not None
            file_path = os.path.join(settings.task_dir, task_view.id.hex + ".blend")
            assert os.path.isfile(file_path)
            async with aiofiles.open(file_path, "rb") as out_file:
                file_data = await out_file.read()
                assert file_data == file_bytes
            assert await Task.filter(id=task_view.id) is not None
        assert len(await Task.all()) == 10

    async def test_create_rollback(self) -> None:
        os.removedirs(settings.task_dir)
        task = random_task_data()
        with pytest.raises(FileNotFoundError):
            await tasks.create(task)
        assert len(await Task.all()) == 0
        os.makedirs(settings.task_dir)

    async def test_get_without_data(self) -> None:
        tasks_data = await tasks.get()
        assert len(tasks_data) == 0
