from typing import Dict, Optional

from config import DIR, URL, Settings


class BinaryData:
    def __init__(self, version: str, url: str):
        self.version = version
        self.url = url


class AppState:
    def __init__(self) -> None:
        self.directories: Optional[DIR] = None
        self.urls: Optional[URL] = None
        self.settings: Optional[Settings] = None
        self.tasks: Dict[str, bytes] = {}
        self.latest_version: Optional[BinaryData] = None
