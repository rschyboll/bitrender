from uuid import UUID
import re

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
        self.__parse_samples(message)

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

    def __parse_samples(self, message: ProcessMessage) -> None:
        regex = r"Sample (\d*)/"
        match = re.search(regex, message.text, re.MULTILINE)
        if match is not None:
            value = match.groups()[0]
            if value.isdigit():
                self.samples = int(value)


class TaskData(BaseModel):
    task_id: UUID
    subtask_id: UUID
    frame_nr: int
    samples_offset: int
    time_limit: int
    max_samples: int
    resolution_x: int
    resolution_y: int
