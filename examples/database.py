"""Demo showing Kew workers sharing a database connection."""

from __future__ import annotations

import asyncio as aio
from typing import Any

import aiofiles
from pymongo import AsyncMongoClient, errors

from kewkew import Kew


class MyKew(Kew):
    """Kew subclass for MongoDB updates."""

    # Shared resources can be applied to the Kew class at init
    # It is not required to have workers and maxsize args if using the defaults
    def __init__(self, conn: AsyncMongoClient, workers: int = 3, maxsize: int | None = None):
        super().__init__(workers, maxsize)
        self.conn = conn

    # Kew child classes must implement a worker method
    # This method is given data from the queue and must return a boolean
    # Kew uses this success boolean to mark queue items as complete
    async def worker(self, data: tuple[str, Any]) -> bool:
        """Worker uses queue data and shared conn to make db updates."""
        key, value = data
        find = {"key": key}
        update = {"$set": {"value": value}}
        try:
            await self.conn.data.coll.update_one(find, update, upsert=True)
        except errors.PyMongoError:
            async with aiofiles.open("failed.txt", "a") as fout:
                await fout.write(f"{key}, {value}\n")
            return False
        return True


async def main():
    """Demo main updates a database via a Kew."""
    # Create the db connection
    # Async clients should be init'd inside of an async scope
    conn = AsyncMongoClient("mongodb://user:password@loc.test.com:12345")

    # Create the Kew with db conn so the workers have access to it
    kew = MyKew(conn)

    # Load data into the Kew
    data = {"a": 1, "b": 2, "c": 3}
    for pair in data.items():
        await kew.add(pair)

    # Wait for the Kew to finish processing the data
    await kew.finish()


if __name__ == "__main__":
    aio.run(main())
