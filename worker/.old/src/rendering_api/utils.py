from __future__ import annotations
import json
import sys
from typing import Any, List, Optional, TypedDict

import bpy


class MergeTask(TypedDict):
    samples: int
    subtask_id: str


class Args:
    def __init__(
        self,
        task: Optional[str] = None,
        frame_nr: Optional[int] = None,
        samples: Optional[int] = None,
        offset: Optional[int] = None,
        res_x: Optional[int] = None,
        res_y: Optional[int] = None,
        output: Optional[str] = None,
        time_limit: Optional[int] = None,
        merge_files: Optional[list[MergeTask]] = None,
        files_dir: Optional[str] = None,
        **__: Any,
    ):
        self.task = task
        self.frame_nr = frame_nr
        self.samples = samples
        self.offset = offset
        self.res_x = res_x
        self.res_y = res_y
        self.output = output
        self.time_limit = time_limit
        self.merge_files = merge_files
        self.files_dir = files_dir

    @classmethod
    def from_sys_args(cls) -> Args:
        json_data = json.loads(sys.argv[5])
        if (
            "task" in json_data and isinstance(json_data["task"], str)
        ) or "merge_files" in json_data:
            return cls(**json_data)
        raise KeyError()


def setup_devices() -> None:
    addons = bpy.context.preferences.addons
    cycles_preferences = addons["cycles"].preferences
    cuda_devices = cycles_preferences.get_devices_for_type("CUDA")
    optix_devices = cycles_preferences.get_devices_for_type("OPTIX")
    if len(optix_devices) != 0:
        bpy.context.preferences.addons[
            "cycles"
        ].preferences.compute_device_type = "OPTIX"
        bpy.context.scene.cycles.device = "GPU"
        disable_devices(cuda_devices)
        for device in optix_devices:
            if device.type != "CPU":
                device.use = True
            else:
                device.use = False
    elif len(cuda_devices) != 0:
        bpy.context.preferences.addons[
            "cycles"
        ].preferences.compute_device_type = "CUDA"
        bpy.context.scene.cycles.device = "GPU"
        for device in cuda_devices:
            if device.type != "CPU":
                device.use = True
            else:
                device.use = False


def disable_devices(devices: List[Any]) -> None:
    for device in devices:
        device.use = False
