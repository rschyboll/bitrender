import os
import sys

# If we are running from the pyfuse3 source directory, try
# to load the module from there first.
basedir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
if os.path.exists(os.path.join(basedir, "setup.py")) and os.path.exists(
    os.path.join(basedir, "src", "pyfuse3.pyx")
):
    sys.path.insert(0, os.path.join(basedir, "src"))

from argparse import ArgumentParser
import stat
import logging
import errno
import pyfuse3
import pyfuse3_asyncio
import asyncio

pyfuse3_asyncio.enable()

try:
    import faulthandler
except ImportError:
    pass
else:
    faulthandler.enable()

log = logging.getLogger(__name__)


class TestFs(pyfuse3.Operations):
    def __init__(self, files):
        super(TestFs, self).__init__()
        self.files = files
        self.hello_name = b"message"
        self.hello_inode = pyfuse3.ROOT_INODE + 1
        self.hello_data = b"hello world\n"

    async def getattr(self, inode, ctx=None):
        entry = pyfuse3.EntryAttributes()
        if inode == pyfuse3.ROOT_INODE:
            entry.st_mode = stat.S_IFDIR | 0o755
            entry.st_size = 0
        elif inode <= pyfuse3.ROOT_INODE + len(self.files):
            entry.st_mode = stat.S_IFREG | 0o644
            entry.st_size = len(self.files[inode - 1 - pyfuse3.ROOT_INODE]["data"])
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

    async def lookup(self, parent_inode, name, ctx=None):
        if (
            parent_inode != pyfuse3.ROOT_INODE
            or parent_inode >= pyfuse3.ROOT_INODE + len(self.files)
        ):
            raise pyfuse3.FUSEError(errno.ENOENT)
        return self.getattr(self.hello_inode)

    async def opendir(self, inode, ctx):
        if inode != pyfuse3.ROOT_INODE:
            raise pyfuse3.FUSEError(errno.ENOENT)
        return inode

    async def readdir(self, fh, start_id, token):
        assert fh == pyfuse3.ROOT_INODE

        for file in self.files:
            if file["inode"] <= start_id:
                continue

            if not pyfuse3.readdir_reply(
                token,
                file["name"].encode(),
                await self.getattr(file["inode"]),
                file["inode"] + 1,
            ):
                break

        return

    async def open(self, inode, flags, ctx):
        if flags & os.O_RDWR or flags & os.O_WRONLY:
            raise pyfuse3.FUSEError(errno.EACCES)
        return pyfuse3.FileInfo(fh=inode)

    async def read(self, fh, off, size):
        data = self.files[fh - 1 - pyfuse3.ROOT_INODE]["data"]
        if len(data) < size:
            return data

        return self.files[fh - 1 - pyfuse3.ROOT_INODE]["data"]


async def test():
    files = [
        {"name": "test", "data": b"brewrwer\n", "inode": pyfuse3.ROOT_INODE + 1},
        {"name": "test2", "data": b"brewrwer3\n", "inode": pyfuse3.ROOT_INODE + 2},
    ]

    testfs = TestFs(files)
    fuse_options = set(pyfuse3.default_options)
    fuse_options.add("fsname=hello")
    fuse_options.add("debug")

    pyfuse3.init(testfs, "./test", fuse_options)
    task = asyncio.create_task(pyfuse3.main())
    i = 1
    while True:
        print("TEST")
        await asyncio.sleep(10)
        files.append(
            {
                "name": "test2" + str(i),
                "data": b"brewrwer3\n",
                "inode": pyfuse3.ROOT_INODE + 2 + i,
            },
        )
        i += 1
        if i == 4:
            break
    pyfuse3.terminate()
    await task
    pyfuse3.close()


def main():
    asyncio.run(test())


if __name__ == "__main__":
    main()
