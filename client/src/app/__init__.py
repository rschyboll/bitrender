from abc import ABC, abstractmethod
from aiohttp import ClientSession

from errors import UserException


class App(ABC):
    def __init__(self) -> None:
        self.session = ClientSession()

    async def run(self) -> None:
        try:
            await self._run()
        except UserException as error:
            await self._rollback()
            self.__print_error(error)
        except Exception:
            await self._rollback()
            raise
        finally:
            await self.__close_session()

    def __print_error(self, error: UserException) -> None:
        if error.message is not None:
            print(error.message)
        if error.context is not None:
            print(error.context)

    @abstractmethod
    async def _run(self) -> None:
        raise NotImplementedError()

    async def __close_session(self) -> None:
        await self.session.close()

    @abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError()
