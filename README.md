# kewkew

A tiny queue library leveraging asyncio for background tasks or scripting

## Install

You can install `kewkew` via pip.

```bash
python -m pip install kewkew
```

You can also download the `kewkew.py` source from this repo. There are no external dependencies to worry about.

## Usage

The `Kew` class is meant to be a parent class. At a minimum, the child class needs to implement an async worker method which must do two things:

- Take a single argument that accepts data from the queue
- Returns a boolean if the data was processed successfully and can be removed from the queue

Here is a minimum viable implementation.

```python
from kewkew import Kew

class MyKew(Kew):
    async def worker(data: object) -> bool:
        print(data)
        return True
```

We then have two main ways of using the queue. `Kew` provides both sync and async methods to add items to the queue and tell the queue to finish processing (for a graceful shutdown).

This first example uses the sync calls so everything can be run in an interactive environment.

```python
from mykew import MyKew

kew = MyKew()
for i in range(100):
    kew.add_sync(i)
kew.finish_sync()
```

This second example uses the async calls within a coroutine.

```python
import asyncio as aio

async def main():
    kew = MyKew()
    for i in range(100):
        await kew.add(i)
    await kew.finish()

aio.run(main)
```

You can see this and an async database processing example in the [examples folder](examples/).
