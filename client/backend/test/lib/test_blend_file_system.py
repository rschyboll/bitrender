# pylint: disable=import-error
import os
import pytest
from src.lib.blend_file_system import BlendFileSystem

class TestBlendFileSystem:
    def setup_method(self, test_blend_file: bytearray):
        self.blend_file_system = BlendFileSystem(test_blend_file)

    def test_init(self, test_blend_file: bytearray):
        blend_file_system = BlendFileSystem(test_blend_file)
        assert blend_file_system.blend_file == test_blend_file, "File in blend file system corrupted."
        assert isinstance(blend_file_system.blend_file, bytearray), "File in blend file system has wrong type."

    def test_access(self):
        pass