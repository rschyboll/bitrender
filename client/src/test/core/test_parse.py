# file-ignore: line-too-long

from typing import Tuple

import pytest

from core.parse import parse_blender_memory


@pytest.mark.parametrize(
    "blender_log, expected",
    [
        (
            "Fra:1 Mem:8.03M (Peak 8.16M) | Time:00:00.08 | Mem:0.00M,"
            " Peak:0.00M | Scene, View Layer | Waiting for render to start",
            (8.03, 8.16),
        ),
        (
            "Fra:1 Mem:12.53M (Peak 23.52M) | Time:00:00.12 | Mem:350.00M, Peak:350.00M | Scene,"
            " View Layer | Updating Geometry BVH Cube 1/1 | Building OptiX acceleration structure",
            (12.53, 23.52),
        ),
        (
            "Fra:1 Mem:44.19M (Peak 44.19M) | Time:00:00.13 | Remaining:00:07.01"
            " | Mem:381.91M, Peak:381.91M | Scene, View Layer | Sample 1/1024",
            (44.19, 44.19),
        ),
        (
            "Fra:1 Mem:75.85M (Peak 107.49M) | Time:00:06.14 | Mem:381.93M,"
            " Peak:381.93M | Scene, View Layer | Finished",
            (75.85, 107.49),
        ),
        (
            "Fra:2 Mem:5037.19M (Peak 5037.20M) | Time:00:09.82 | Remaining:-14:-08.-48 |"
            " Mem:3044.05M, Peak:3044.05M | Scene, Full | Sample 129/15000",
            (5037.19, 5037.20),
        ),
        (
            "Fra:2 Mem:2962.00M (Peak 4239.91M) | Time:00:05.22 | Mem:883.00M, Peak:953.80M |"
            " Scene, Full | Updating Geometry BVH sheet.009 255/442 | Building BVH",
            (2962.00, 4239.91),
        ),
    ],
)
def test_parse_blender_memory(blender_log: str, expected: Tuple[float, float]) -> None:
    memory = parse_blender_memory(blender_log)
    assert memory == expected
