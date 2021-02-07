import pytest

blend_test_file_path = "./test/content/blend_test_file.blend"

@pytest.fixture
def test_blend_file():
    with open(blend_test_file_path, "rb") as blend_file:
        blend_file_content = blend_file.read()
    blend_file_content = bytearray(blend_file_content)
    return blend_file_content