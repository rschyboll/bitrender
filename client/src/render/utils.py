from __future__ import annotations

import json
import sys
from typing import Any, List, Optional

import bpy


class Args:
    def __init__(
        self,
        task: str,
        samples: Optional[int] = None,
        res_x: Optional[int] = None,
        res_y: Optional[int] = None,
        **__: Any,
    ):
        self.task = task
        self.samples = samples
        self.res_x = res_x
        self.res_y = res_y

    @classmethod
    def from_sys_args(cls) -> Args:
        json_data = json.loads(sys.argv[5])
        if "task" in json_data and isinstance(json_data["task"], str):
            return cls(**json_data)
        raise KeyError()


def setup_devices() -> None:
    addons = bpy.context.preferences.addons
    cycles_preferences = addons["cycles"].preferences
    cuda_devices = cycles_preferences.get_devices_for_type("CUDA")
    optix_devices = cycles_preferences.get_devices_for_type("OPTIX")
    if len(optix_devices) != 0:
        disable_devices(cuda_devices)
        for device in optix_devices:
            if device.type != "CPU":
                device.use = True
            else:
                device.use = False
    elif len(cuda_devices) != 0:
        for device in cuda_devices:
            if device.type != "CPU":
                device.use = True
            else:
                device.use = False


def disable_devices(devices: List[Any]) -> None:
    for device in devices:
        device.use = False
