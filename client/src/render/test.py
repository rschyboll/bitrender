import json
import sys

import bpy
from pathlib import Path

devices = bpy.context.preferences.addons["cycles"].preferences.get_devices_for_type(
    "CUDA"
)
print(devices)


class Args:
    def __init__(self, file: str):
        self.file = file


def parse_args() -> Args:
    __args = json.loads(sys.argv[5])
    file = None
    if "file" in __args:
        file = __args["file"]
    if file is not None:
        return Args(file=file)
    raise Exception()


args = parse_args()
