import json
import os
import shutil
import tarfile
from asyncio import TimeoutError as AsyncioTimeout
from json import JSONDecodeError
from typing import Any, Generator

from aiohttp import ClientError

from app.action import Action
from app.state import BinaryData
from config import DIR, URL, Settings
from errors.binary import BinaryVersionCheckError, OSSaveError
from errors.connection import ConnectionException


class UpdateBinary(Action[None]):
    critical = True
    background = False

    def __init__(self, settings: Settings, urls: URL, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls

    async def _start(self) -> None:
        self.state.latest_version = await self.__get_latest_version()
        if self.state.latest_version.version != self.settings.blender_version:
            await self.run_subaction(DownloadBinary)
            await self.run_subaction(UnpackBinary)
            self.settings.blender_version = self.state.latest_version.version
            self.settings.save()

    async def __get_latest_version(self) -> BinaryData:
        try:
            async with self.session.get(self.urls.binary) as response:
                if response.status != 200:
                    raise BinaryVersionCheckError()
                data = await response.text()
                decoded_data = json.loads(data)
                return self.__parse_version_data(decoded_data)
        except (ClientError, AsyncioTimeout) as error:
            raise ConnectionException() from error
        except (JSONDecodeError, KeyError, ValueError) as error:
            raise BinaryVersionCheckError() from error

    def __parse_version_data(self, data: Any) -> BinaryData:
        if isinstance(data, dict) and "version" in data and "url" in data:
            version = data["version"]
            url = data["url"]
            if isinstance(version, str) and isinstance(url, str):
                return BinaryData(version, url)
        raise BinaryVersionCheckError()

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pass


class DownloadBinary(Action[None]):
    critical = True
    background = False

    def __init__(self, directories: DIR, latest_version: BinaryData, **kwargs: Any):
        super().__init__(**kwargs)
        self.latest_version = latest_version
        self.directories = directories

    async def _start(self) -> None:
        await self.__download_binary(
            self.latest_version.url, self.directories.download_file
        )

    async def __download_binary(self, url: str, file_path: str) -> None:
        try:
            async with self.session.get(url) as response:
                with open(file_path, "wb+") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        file.write(chunk)
        except (ClientError, AsyncioTimeout) as error:
            raise ConnectionException() from error
        except OSError as error:
            raise OSSaveError() from error

    async def _local_rollback(self) -> None:
        if os.path.exists(self.directories.download_file):
            os.remove(self.directories.download_file)

    async def _rollback(self) -> None:
        if os.path.exists(self.directories.download_file):
            os.remove(self.directories.download_file)


class UnpackBinary(Action[None]):
    critical = True
    background = False

    def __init__(self, settings: Settings, urls: URL, directories: DIR, **kwargs: Any):
        super().__init__(**kwargs)
        self.settings = settings
        self.urls = urls
        self.directories = directories

    async def _start(self) -> None:
        assert os.path.exists(self.directories.download_file)
        binary_tar = tarfile.open(self.directories.download_file)
        self._remove_old_binary()
        sub_folder = self._get_sub_folder(binary_tar)
        binary_tar.extractall(
            path=self.directories.binary_dir,
            members=self.members(binary_tar, sub_folder),
        )
        self._remove_download_file()

    def _get_sub_folder(self, file: tarfile.TarFile) -> str:
        names = file.getnames()
        return os.path.commonprefix(names)

    def members(
        self, file: tarfile.TarFile, sub_folder: str
    ) -> Generator[tarfile.TarInfo, None, None]:
        folder_name_length = len(sub_folder)
        for member in file.getmembers():
            if member.path.startswith(sub_folder):
                member.path = member.path[folder_name_length:]
                yield member

    async def _local_rollback(self) -> None:
        if os.path.exists(self.directories.binary_dir):
            shutil.rmtree(self.directories.binary_dir)

    def _remove_old_binary(self) -> None:
        if os.path.exists(self.directories.binary_dir):
            shutil.rmtree(self.directories.binary_dir)
        os.mkdir(self.directories.binary_dir)

    def _remove_download_file(self) -> None:
        if os.path.exists(self.directories.download_file):
            os.remove(self.directories.download_file)

    async def _rollback(self) -> None:
        pass
