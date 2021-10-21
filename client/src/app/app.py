from typing import List

from app.actions import Action


class App:
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.finished_actions: List[Action] = []

    async def run(self):
        pass

    async def start_action(self):
        pass
