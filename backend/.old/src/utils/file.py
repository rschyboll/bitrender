import os
from typing import TYPE_CHECKING, List
from zipfile import ZipFile

import aiofiles
from fastapi import UploadFile

from config import Settings

if TYPE_CHECKING:
    from models import Frame, Task
else:
    Frame = object
    Task = object


async def save_file(path: str, file: UploadFile) -> None:
    async with aiofiles.open(path, "wb+") as file_stream:
        while content := await file.read(1024):
            if isinstance(content, bytes):
                await file_stream.write(content)
            elif isinstance(content, str):
                await file_stream.write(content.encode())


async def move_file(source_path: str, dest_path: str) -> None:
    async with aiofiles.open(source_path, "rb") as source_stream:
        async with aiofiles.open(dest_path, "wb+") as dest_stream:
            await dest_stream.write(await source_stream.read())
    os.remove(source_path)


async def create_frames_zip(
    task: Task, frames: List[Frame], dest: str, settings: Settings
) -> None:
    with ZipFile(os.path.join(settings.task_dir, task.id.hex + ".zip")) as zipObj:
        for frame in frames:
            file = settings.get_frame_path(frame.id)
