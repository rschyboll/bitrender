import bpy


bpy.ops.wm.open_mainfile(filepath="/home/hoodrobinrs/Desktop/Blenderman.blend")


bpy.ops.render.render(animation=False, write_still=False)
