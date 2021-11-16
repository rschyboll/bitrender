from fastapi_websocket_rpc import RpcMethodsBase


class TasksService(RpcMethodsBase):
    async def task_status(self) -> None:
        print(self.channel)


class Taskall:
    pass
