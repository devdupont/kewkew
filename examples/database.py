"""
Demo showing Kew workers sharing a database connection
"""

import asyncio as aio

# motor is an async MongoDB client
from motor import MotorClient

from kewkew import Kew


class MyKew(Kew):

    # Shared resources can be applied to the Kew class at init
    # It is not required to have workers and maxsize args if using the defaults
    def __init__(self, conn: MotorClient, workers: int = 3, maxsize: int = None):
        super().__init__(workers, maxsize)
        self.conn = conn

    # Kew child classes must implement a worker method
    # This method is given data from the queue and must return a boolean
    # Kew uses this success boolean to mark queue items as complete
    async def worker(self, data: object) -> bool:
        """
        Worker uses queue data and shared conn to make db updates
        """
        key, value = data
        try:
            find = {"key": key}
            update = {"$set": {"value": value}}
            await self.conn.data.coll.update_one(find, update, upsert=True)
            return True
        except:
            print(key, value, file=open("failed.txt", "a"))
            return False


async def main():
    """
    Demo main updates a database via a Kew
    """
    # Create the db connection
    # Async clients should be init'd inside of an async scope
    conn = MotorClient("mongodb://user:password@loc.test.com:12345")

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
