import os
import time
from typing import Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enforce_types import enforce_types

@enforce_types
@dataclass_json
@dataclass
class BlendFile:
    """Blend file class"""
    data: bytearray = field(repr=False)
    name: str
    size: int = field(init=False)
    readable: bool = field(default=True, init=False)
    pipe: Tuple[int, int] = field(init=False)
    create_time: float = field(init=False)

    def __post_init__(self):
        self.size = len(self.data)
        self.pipe = os.pipe()
        self.create_time = time.time()

    def get_name(self):
        return self.name

    def get_create_time(self):
        return self.create_time
    
    def get_size(self):
        return self.size

    def open(self, flags):
        if self.readable:
            return self.pipe[0]
        else:
            return -1

    def read(self, length, offset, fh):
        if self.readable:
            return bytes(self.data[offset: offset + length])
        else:
            return 0