from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from fastapi_websocket_rpc import WebSocketRpcClient

    from config import DIR, URL, Settings
    from services import RPCCall
else:
    WebSocketRpcClient = object
    DIR = object
    URL = object
    Settings = object
    RPCCall = object


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
        self.output_files: Dict[str, bytes] = {}
        self.latest_version: Optional[BinaryData] = None
        self.rpc_client: Optional[WebSocketRpcClient] = None
        self.rpc_call: Optional[RPCCall]
