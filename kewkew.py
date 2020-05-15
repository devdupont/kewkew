"""
A tiny Queue library leveraging asyncio
"""

import asyncio as aio
from abc import ABCMeta, abstractmethod


class Kew(metaclass=ABCMeta):
    """
    An asyncio Queue wrapper with a simple interface

    Child class must implement an async worker method
    """

    _num_workers: int
    _queue: aio.Queue
    _workers: [aio.Task]

    def __init__(self, workers: int = 3, maxsize: int = 0):
        self._num_workers = workers
        self._queue = aio.Queue(maxsize=maxsize)
        self._workers = [aio.create_task(self._worker()) for _ in range(workers)]

    async def _worker(self):
        """
        Worker thread wrapper handling queue pulling
        """
        while True:
            data = await self._queue.get()
            success = await self.worker(data)
            if success:
                self._queue.task_done()

    @abstractmethod
    async def worker(self, data: object) -> bool:
        """
        Worker handler is given data from the queue

        Must return a boolean indicating success
        """
        return True

    async def add(self, data: object):
        """
        Add data to the queue
        
        Awaits until there is room if a max size is set
        """
        await self._queue.put(data)

    def add_sync(self, data: object):
        """
        Add data to the queue immediately

        Raises a QueueFull exception if no room when a max size is set
        """
        self._queue.put_nowait(data)

    async def finish(self, wait: bool = True):
        """
        Tells the queue to shutdown gracefully

        If wait, the queue will continue processing until empty
        """
        if wait:
            while not self._queue.empty():
                await aio.sleep(0.01)
        for worker in self._workers:
            worker.cancel()
        await aio.gather(*self._workers, return_exceptions=True)

    def finish_sync(self, wait: bool = True):
        """
        Tells the queue to shutdown gracefully

        If wait, the queue will continue processing until empty
        """
        aio.run(self.finish(wait))

    def __len__(self) -> int:
        return len(self._queue)
