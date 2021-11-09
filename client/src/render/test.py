# pylint: disable=wrong-import-position
import os
import sys

import bpy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from render.utils import Args, setup_devices

args = Args.from_sys_args()
setup_devices()

bpy.ops.wm.open_mainfile(filepath=args.task)

bpy.ops.render.render()
