import aiofiles
from fastapi import UploadFile


async def save_file(path: str, file: UploadFile) -> None:
    async with aiofiles.open(path, "wb+") as file_stream:
        while content := await file.read(1024):
            if isinstance(content, bytes):
                await file_stream.write(content)
            elif isinstance(content, str):
                await file_stream.write(content.encode())
