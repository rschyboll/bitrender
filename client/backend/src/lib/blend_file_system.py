import os
import stat
import ntpath
import errno
from fuse import FUSE, FuseOSError, Operations
from blend_file import BlendFile

class BlendFileSystem(Operations):
    """Blend file system class"""

    def __init__(self, mounting_point: str):
        self.mounting_point = mounting_point
        self.files = {}

    def addFile(self, blend_file: BlendFile):
        self.files[blend_file.get_name()] = blend_file

    def removeFile(self, blend_file: BlendFile):
        file_name = blend_file.get_name()
        if file_name in self.files:
            del self.files[file_name]

    def __get_filename(self, path: str) -> str:
        return ntpath.basename(path).split(".")[0]


    # Filesystem methods
    # ==================

    def access(self, path, mode):
        pass

    def readdir(self, path, fh) -> str:
        dirents = ['.', '..']
        files = []
        if path == "/":
            for blend_file in self.files.values():
                files.append(blend_file.get_name() + ".blend")
        dirents.extend(files)
        for r in dirents:
            yield r

    def getattr(self, path, fh=None) -> dict:
        if path == "/":
            return {'st_mode': stat.S_IFDIR}
        file_name = self.__get_filename(path)
        if file_name in self.files:
            blend_file = self.files[file_name]
            attr = {
                   'st_mode': 33188, 'st_size': blend_file.get_size()}
            return attr
        return {}

    # File methods
    # ============

    def open(self, path, flags) -> int:
        file_name = self.__get_filename(path)
        if file_name in self.files:
            return self.files[file_name].open(flags)

    def read(self, path, length, offset, fh) -> bytes:
        file_name = self.__get_filename(path)
        if file_name in self.files:
            return self.files[file_name].read(length, offset, fh)

if __name__ == "__main__":
    file_system = BlendFileSystem("./test")
    with open("/home/hoodrobinrs/Dokumenty/Rendering_Server/client/backend/test/content/blend_test_file.blend", "rb") as blend_file:
        blend_file_data = blend_file.read()
    blend_file = BlendFile(bytearray(blend_file_data), "test")
    file_system.addFile(blend_file)
    FUSE(file_system, "./test", nothreads=True, foreground=True)
    