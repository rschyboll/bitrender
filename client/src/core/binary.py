import json
import os
import shutil
import tarfile
from json.decoder import JSONDecodeError

import aiohttp
from config import DIR, URL, Settings

from core.settings import (
    binary_dir,
    load_current_version,
    save_current_version,
    temp_file_path,
)
from errors.binaries import OSSaveError
from errors.connection import ConnectionException


class Binary:
    def __init__(self, directories: DIR, settings: Settings, urls: URL):
        self.directories = directories
        self.settings = settings
        self.urls = urls


async def up_to_date(server_ip: str) -> bool:
    url = server_ip + "/binaries/latest"
    version_tuple = await load_current_version()
    if version_tuple is None:
        return False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                decoded_data = json.loads(data)
                if decoded_data["version"] != version_tuple[0]:
                    return False
                return True
    except (aiohttp.ClientError) as error:
        raise ConnectionException from error


async def update_binary(server_ip: str) -> None:
    url = server_ip + "/binaries/latest"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                decoded_data = json.loads(data)
                url = decoded_data["url"]
                version = decoded_data["version"]
                await download_binary(url)
                await save_current_version(version, url)
    except (
        OSError,
        TypeError,
        ValueError,
        JSONDecodeError,
        aiohttp.ClientError,
    ) as error:
        raise ConnectionException from error


async def download_binary(url: str) -> None:
    print("Pobieranie plików blendera, proszę czekać")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(temp_file_path, "wb+") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        file.write(chunk)
        copy_binary_to_binary_dir()
    except (aiohttp.ClientError, OSError) as error:
        rollback_download_binary()
        if isinstance(error, OSError):
            raise OSSaveError() from error
        raise ConnectionException from error


def rollback_download_binary() -> None:
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    except OSError:
        return


def copy_binary_to_binary_dir() -> None:
    try:
        tar = tarfile.open(temp_file_path)

        os.mkdir(binary_dir + "tmp")
        tar.extractall(binary_dir + "tmp")
        os.remove(temp_file_path)

        if os.path.exists(binary_dir):
            shutil.rmtree(binary_dir)

        shutil.copytree(
            os.path.join(binary_dir + "tmp", os.listdir(binary_dir + "tmp")[0]),
            binary_dir,
        )
        shutil.rmtree(binary_dir + "tmp")
    except (OSError, ValueError) as error:
        rollback_copy_binary()
        raise OSSaveError() from error


def rollback_copy_binary() -> None:
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(binary_dir):
            shutil.rmtree(binary_dir)
        if os.path.exists(binary_dir + "tmp"):
            shutil.rmtree(binary_dir + "tmp")
    except OSError:
        return
