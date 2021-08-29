from typing import NamedTuple


class Config:
    app_name = "rendering_server_worker"
    app_author = "hoodrobinrs"
    settings_file = "settings.json"
    binary_directory = "blender/"


class Settings(NamedTuple):
    token: str
    name: str
    server_ip: str
