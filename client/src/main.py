import asyncio

from lib.blender_subprocess import BlenderSubprocess

BIN_PATH = '/home/hoodrobinrs/Desktop/blender-2.92.0-linux64/blender'
SCRIPT_PATH = '/home/hoodrobinrs/Documents/Rendering_Server/client/src/blender-rendering-api/src/main.py'
CONFIG_PATH = '/home/hoodrobinrs/Documents/Rendering_Server/client/src/config'

async def subprocess_listener():
    subprocess = BlenderSubprocess(BIN_PATH, SCRIPT_PATH, CONFIG_PATH)
    async with subprocess:
        while subprocess.running or not subprocess.is_empty():
            message = await subprocess.receive()
            print(message)

async def main():
    task = asyncio.create_task(subprocess_listener())
    await task

asyncio.run(main())
