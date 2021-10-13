from abc import ABC, abstractmethod

from aiohttp import ClientSession

from errors import UserError


class App(ABC):
    async def run(self) -> None:
        async with ClientSession() as session:
            try:
                await self._run(session)
            except UserError as error:
                await self._rollback()
                self.__print_error(error)
            except Exception:
                await self._rollback()
                raise

    def __print_error(self, error: UserError) -> None:
        if error.message is not None:
            print(error.message)
        if error.context is not None:
            print(error.context)

    @abstractmethod
    async def _run(self, session: ClientSession) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError()
