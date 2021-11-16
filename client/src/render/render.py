# pylint: disable=wrong-import-position
import os
import sys

import bpy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from render.utils import Args, setup_devices
from render.output import create_outputs

args = Args.from_sys_args()
setup_devices()

bpy.ops.wm.open_mainfile(filepath=args.task)

context = bpy.context

if args.samples is not None:
    context.scene.cycles.samples = args.samples
if args.output is not None:
    create_outputs(context, args.output)

bpy.ops.render.render()
