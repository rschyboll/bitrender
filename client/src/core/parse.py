import re
from datetime import timedelta
from typing import Optional, Tuple


def parse_blender_memory(log: str) -> Optional[Tuple[float, float]]:
    regex = r"Mem:(\d+\.?\d+?.) \(Peak (\d+.\d+.)\)"
    match = re.findall(regex, log)
    if len(match) == 1 and len(match[0]) == 2:
        mem = match[0][0]
        peak = match[0][1]
        if isinstance(mem, str) and isinstance(peak, str):
            if not mem[-1].isnumeric():
                mem = mem[:-1]
            if not peak[-1].isnumeric():
                peak = peak[:-1]
            return (float(mem), float(peak))
    return None


def parse_render_memory(log: str) -> Optional[Tuple[float, float]]:
    pass


def parse_sample(log: str) -> Optional[int]:
    pass


def parse_time(log: str) -> Optional[timedelta]:
    pass


def parse_remaining_time(log: str) -> Optional[timedelta]:
    pass


def parse_status(log: str) -> Optional[str]:
    pass
