import json
import os
import shutil
import tarfile
from json.decoder import JSONDecodeError
from typing import Any, Optional, TypedDict
import tempfile

from asyncio import TimeoutError
from aiohttp import ClientSession, ClientError
from config import DIR, URL, Settings
from errors.binaries import OSSaveError
from errors.connection import ConnectionException, WrongResponseException


class BinaryData(TypedDict):
    version: str
    url: str


class Binary:
    def __init__(self, directories: DIR, settings: Settings, urls: URL):
        self.directories = directories
        self.settings = settings
        self.urls = urls
        self.__server_binary_data: Optional[BinaryData] = None

    async def __get_server_binary_data(self, session: ClientSession) -> BinaryData:
        server_binary_data = self.__server_binary_data
        if server_binary_data is None:
            server_binary_data = await self.__get_version_data(session)
            self.__server_binary_data = server_binary_data
        return server_binary_data

    def exists(self) -> bool:
        try:
            return os.path.exists(self.directories.binary)
        except OSError:
            return False

    async def up_to_date(self, session: ClientSession) -> bool:
        current_version = self.settings.blender_version
        if current_version is not None:
            server_binary_data = await self.__get_server_binary_data(session)
            return current_version == server_binary_data["version"]
        else:
            return False

    async def __get_version_data(self, session: ClientSession) -> BinaryData:
        try:
            async with session.get(self.urls.binary) as response:
                if response.status != 200:
                    raise WrongResponseException()
                data = await response.text()
                decoded_data = json.loads(data)
                return self.__parse_version_data(decoded_data)
        except (ClientError, TimeoutError) as error:
            raise ConnectionException() from error
        except (JSONDecodeError, KeyError, ValueError) as error:
            raise WrongResponseException() from error

    def __parse_version_data(self, version_data: Any) -> BinaryData:
        if (
            isinstance(version_data, dict)
            and "version" in version_data
            and "url" in version_data
        ):
            version = version_data["version"]
            url = version_data["url"]
            if isinstance(version, str) and isinstance(url, str):
                return {"version": version, "url": url}
        raise WrongResponseException()

    async def download_new_version(self, session: ClientSession) -> None:
        print("Downloading new blender binaries, please wait...")
        tempdir = tempfile.mkdtemp()
        temp_file = self.directories.binary_tar(tempdir)
        server_binary_data = await self.__get_server_binary_data(session)
        await self.__download_binary(session, server_binary_data["url"], temp_file)
        self.__unpack_binary(temp_file)
        shutil.rmtree(tempdir)
        self.settings.blender_version = server_binary_data["version"]
        self.settings.save()

    async def __download_binary(
        self, session: ClientSession, url: str, file_path: str
    ) -> None:
        try:
            async with session.get(url) as response:
                with open(file_path, "wb+") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        file.write(chunk)
        except (ClientError, TimeoutError) as error:
            raise ConnectionException() from error
        except OSError as error:
            raise OSSaveError() from error

    def __unpack_binary(self, packed_binary: str) -> None:
        try:
            tempdir = tempfile.mkdtemp()
            binary_tar = tarfile.open(packed_binary)
            if os.path.exists(self.directories.binary_dir):
                shutil.rmtree(self.directories.binary_dir)
            os.mkdir(self.directories.binary_dir)
            binary_tar.extractall(tempdir)
            binary_temp_dir = os.path.join(tempdir, os.listdir(tempdir)[0])
            shutil.copytree(
                binary_temp_dir, self.directories.binary_dir, dirs_exist_ok=True
            )
            shutil.rmtree(tempdir)
        except OSError as error:
            raise OSSaveError() from error

    def delete(self) -> None:
        if os.path.exists(self.directories.binary_dir):
            shutil.rmtree(self.directories.binary_dir)
        self.settings.blender_version = None
        self.settings.save()
