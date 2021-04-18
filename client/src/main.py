import asyncio

from bpy_subprocess import BPYSubprocess




async def subprocess_listener():
    subprocess = BPYSubprocess("/home/hoodrobinrs/Documents/Rendering_Server/Blender-Rendering-Api/src/main.py", file="/home/hoodrobinrs/Documents/Rendering_Server/Blender-Rendering-Api/src/test.blend")
    async with subprocess:
        while subprocess.running:
            message = await subprocess.receive()
            print(message)
    print("ENDED")

async def main():
    task = asyncio.create_task(subprocess_listener())
    await task

asyncio.run(main())
