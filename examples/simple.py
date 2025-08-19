"""Demo printing to console."""

from kewkew import Kew


class MyKew(Kew):
    """Kew subclass for printing to console."""

    # Kew child classes must implement a worker method
    # This method is given data from the queue and must return a boolean
    # Kew uses this success boolean to mark queue items as complete
    async def worker(self, data: object) -> bool:
        """Worker prints data and returns success."""
        print(data)
        return True


async def a_main():
    """Demo async main prints values via a Kew."""
    kew = MyKew()

    # Load data into the Kew with async add
    for i in range(100):
        await kew.add(i)

    # Wait for the Kew to finish processing the data
    await kew.finish()


def main():
    """Demo sync main prints values via a Kew."""
    kew = MyKew()

    # Load data into the Kew with sync add_sync
    for i in range(100):
        kew.add_sync(i)

    # Wait for the Kew to finish processing the data
    kew.finish_sync()


if __name__ == "__main__":
    # We can run the sync main
    main()

    # Or we can run the async main using aio.run
    # import asyncio as aio
    # aio.run(a_main())
