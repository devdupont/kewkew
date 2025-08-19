"""A tiny Queue library leveraging asyncio."""

from __future__ import annotations

import asyncio as aio
from abc import ABCMeta, abstractmethod
from typing import Any


class Kew(metaclass=ABCMeta):
    """An asyncio Queue wrapper with a simple interface.

    Child class must implement an async worker method.
    """

    _num_workers: int
    _queue: aio.Queue
    _workers: list[aio.Task]

    def __init__(self, workers: int = 3, maxsize: int = 0):
        self._num_workers = workers
        self._queue = aio.Queue(maxsize=maxsize)
        self._workers = [aio.create_task(self._worker()) for _ in range(workers)]

    async def _worker(self) -> None:
        """Worker thread wrapper handling queue pulling."""
        while True:
            data = await self._queue.get()
            # Catch if user forgot to make worker method async
            success = await self.worker(data) if aio.iscoroutinefunction(self.worker) else self.worker(data)
            if success:
                self._queue.task_done()

    @abstractmethod
    async def worker(self, data: Any) -> bool:
        """Worker handler is given data from the queue.

        Must return a boolean indicating success.
        """
        return True

    async def add(self, data: Any) -> None:
        """Add data to the queue.

        Awaits until there is room if a max size is set.
        """
        await self._queue.put(data)

    def add_sync(self, data: Any) -> None:
        """Add data to the queue immediately.

        Raises a QueueFull exception if no room when a max size is set.
        """
        self._queue.put_nowait(data)

    async def finish(self, *, wait: bool = True) -> None:
        """Tells the queue to shutdown gracefully.

        If wait, the queue will continue processing until empty.
        """
        if wait:
            while not self._queue.empty():
                await aio.sleep(0.01)
        for worker in self._workers:
            worker.cancel()
        await aio.gather(*self._workers, return_exceptions=True)

    def finish_sync(self, *, wait: bool = True) -> None:
        """Tells the queue to shutdown gracefully.

        If wait, the queue will continue processing until empty.
        """
        aio.run(self.finish(wait=wait))

    def __len__(self) -> int:
        return self._queue.qsize()
