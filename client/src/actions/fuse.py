import asyncio
import errno
import os
import shutil
import stat
from asyncio import CancelledError
from typing import Any, Dict, Optional

import pyfuse3
import pyfuse3_asyncio

from app.action import Action
from config import DIR

pyfuse3_asyncio.enable()


class Fuse(Action[None]):
    critical = True
    background = True

    def __init__(self, directories: DIR, tasks: Dict[str, bytes], **kwargs: Any):
        super().__init__(**kwargs)
        self.directories = directories
        self.tasks = tasks
        self.filesystem = FuseFilesystem(tasks)

    async def _start(self) -> None:
        self._create_task_dir()
        fuse_options = set(pyfuse3.default_options)
        pyfuse3.init(self.filesystem, self.directories.task_dir, fuse_options)
        try:
            await pyfuse3.main()
        except CancelledError:
            pyfuse3.close()

    def _create_task_dir(self) -> None:
        if os.path.exists(self.directories.task_dir):
            shutil.rmtree(self.directories.task_dir)
        os.mkdir(self.directories.task_dir)

    async def _local_rollback(self) -> None:
        pass

    async def _rollback(self) -> None:
        pyfuse3.close()
        try:
            shutil.rmtree(self.directories.task_dir)
        except Exception:
            pass


class FuseFile:
    def __init__(self, name: str, inode: int, data: bytes):
        self.name = name
        self.inode = inode
        self.data = data


class FuseFilesystem(pyfuse3.Operations):
    def __init__(self, tasks: Dict[str, bytes]):
        super(FuseFilesystem, self).__init__()
        self.tasks = tasks

    @property
    def files(self) -> Dict[int, FuseFile]:
        files: Dict[int, FuseFile] = {}
        inode: int = pyfuse3.ROOT_INODE + 1
        for task_name, task in self.tasks.items():
            files[inode] = FuseFile(task_name, inode, task)
            inode += 1
        return files

    @property
    def max_inode(self) -> int:
        inode: int = pyfuse3.ROOT_INODE + len(self.tasks)
        return inode

    def find_by_name(self, name: str) -> Optional[FuseFile]:
        files = self.files
        for file in files.values():
            if file.name == name:
                return file
        return None

    async def getattr(self, inode: int, ctx: Any = None) -> pyfuse3.EntryAttributes:
        entry = pyfuse3.EntryAttributes()
        if inode == pyfuse3.ROOT_INODE:
            entry.st_mode = stat.S_IFDIR | 0o755
            entry.st_size = 0
        elif inode > pyfuse3.ROOT_INODE and inode <= self.max_inode:
            entry.st_mode = stat.S_IFREG | 0o644
            entry.st_size = len(self.files[inode].data)
        else:
            raise pyfuse3.FUSEError(errno.ENOENT)

        stamp = int(1438467123.985654 * 1e9)
        entry.st_atime_ns = stamp
        entry.st_ctime_ns = stamp
        entry.st_mtime_ns = stamp
        entry.st_gid = os.getgid()
        entry.st_uid = os.getuid()
        entry.st_ino = inode

        return entry

    async def lookup(
        self, parent_inode: int, name: bytes, ctx: Any = None
    ) -> pyfuse3.EntryAttributes:
        if parent_inode != pyfuse3.ROOT_INODE or name.decode() not in self.tasks:
            raise pyfuse3.FUSEError(errno.ENOENT)
        file = self.find_by_name(name.decode())
        if file is not None:
            return await self.getattr(file.inode)
        raise pyfuse3.FUSEError(errno.ENOENT)

    async def opendir(self, inode: int, ctx: Any) -> int:
        if inode != pyfuse3.ROOT_INODE:
            raise pyfuse3.FUSEError(errno.ENOENT)
        return inode

    async def readdir(self, fh: int, start_id: int, token: Any) -> None:
        assert fh == pyfuse3.ROOT_INODE

        for file in self.files.values():
            if file.inode <= start_id:
                continue
            name = file.name.encode()
            attrs = await self.getattr(file.inode)
            next_id = file.inode + 1
            if not pyfuse3.readdir_reply(token, name, attrs, next_id):
                break
        return

    async def open(self, inode: str, flags: Any, ctx: Any) -> pyfuse3.FileInfo:
        if flags & os.O_RDWR or flags & os.O_WRONLY:
            raise pyfuse3.FUSEError(errno.EACCES)
        return pyfuse3.FileInfo(fh=inode)

    async def read(self, fh: int, off: int, size: int) -> bytes:
        data = self.files[fh].data

        return data[off : off + size]
