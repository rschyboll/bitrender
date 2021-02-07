# pylint: disable=import-error
import os
import pytest
from src.lib.blend_file import BlendFile 

class TestBlendFile:
    def test_init_success(self, test_blend_file: bytearray):
        BlendFile(test_blend_file, "test")

    def test_init_error(self, test_blend_file: bytearray):
        try:
            BlendFile(2, 1, "test")
            assert False, "BlendFile should raise TypeError."
        except TypeError as error:
            assert isinstance(error, TypeError)