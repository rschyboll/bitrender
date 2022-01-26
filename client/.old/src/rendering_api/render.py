# pylint: disable=wrong-import-position
import os
import sys

import bpy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from rendering_api.output import create_outputs
from rendering_api.utils import Args, setup_devices

args = Args.from_sys_args()
setup_devices()

bpy.ops.wm.open_mainfile(filepath=args.task)

context = bpy.context
print(args.__dict__)
if args.samples is not None:
    context.scene.cycles.samples = args.samples
if args.output is not None:
    create_outputs(context, args.output)
if args.time_limit is not None:
    bpy.context.scene.cycles.time_limit = args.time_limit
if args.res_x is not None:
    bpy.context.scene.render.resolution_x = args.res_x
if args.res_y is not None:
    bpy.context.scene.render.resolution_y = args.res_y
if args.offset is not None:
    bpy.context.scene.cycles.sample_offset = args.offset
if args.frame_nr is not None:
    bpy.context.scene.frame_current = args.frame_nr
bpy.context.scene.render.resolution_percentage = 100


bpy.ops.render.render()
