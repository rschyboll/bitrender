import os

import aiofiles
from fastapi import UploadFile


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
            while content := await source_stream.read(1024):
                await dest_stream.write(content)
    os.remove(source_path)
