from uuid import UUID

from pydantic import BaseModel

from core.subprocess import MessageType, ProcessMessage


class TaskStatus:
    def __init__(self) -> None:
        self.finished = False
        self.error = False
        self.no_file = False
        self.samples = 0
        self.memory = 0
        self.time = None
        self.remaining = None

    def update(self, message: ProcessMessage) -> None:
        if message.type == MessageType.STDERR:
            self.error = True
        if self.__finished(message):
            self.finished = True
        if self.__no_file(message):
            self.no_file = True

    def __finished(self, message: ProcessMessage) -> bool:
        if "Finished" in message.text:
            return True
        return False

    def __no_file(self, message: ProcessMessage) -> bool:
        if (
            "Cannot read file" in message.text
            and "No such file or directory" in message.text
        ):
            return True
        return False


class TaskData(BaseModel):
    task_id: UUID
    subtask_id: UUID
    frame_nr: int
    seed: int
    time_limit: int
    max_samples: int
    resolution_x: int
    resolution_y: int
