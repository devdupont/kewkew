"""Kew tests."""

import asyncio as aio

import pytest

from kewkew import Kew


def test_not_implemented() -> None:
    """Test that Kew raises for not-implemented worker method."""

    class TestKew(Kew): ...

    with pytest.raises(TypeError):
        TestKew()  # type: ignore


@pytest.mark.asyncio
async def test_async_queue() -> None:
    class CountKew(Kew):
        counter: int = 0
        total: int = 0

        async def worker(self, data: int) -> bool:
            self.counter += 1
            self.total += data
            return True

    kew = CountKew()
    assert kew.counter == 0
    assert kew.total == 0

    await kew.add(5)
    await aio.sleep(0.01)
    assert kew.counter == 1
    assert kew.total == 5

    await kew.add(10)
    await aio.sleep(0.01)
    assert kew.counter == 2
    assert kew.total == 15

    await kew.finish()
