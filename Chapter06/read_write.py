import asyncio
from enum import Enum

class LockState(Enum):
    IDLE = 0
    READING = 1
    WRITING = 2

class AsyncReadWriteLock:
    def __init__(self):
        self._state = LockState.IDLE
        self._reader_count = 0
        self._writer_waiting = 0 
        self._condition = asyncio.Condition()

    async def read_acquire(self):
        async with self._condition:
            while self._state == LockState.WRITING or self._writer_waiting > 0:
                await self._condition.wait()
            self._reader_count += 1
            self._state = LockState.READING
            print(f"There are {self._reader_count} readers")

    async def read_release(self):
        async with self._condition:
            self._reader_count -= 1
            if self._reader_count == 0:
                self._state = LockState.IDLE
                self._condition.notify_all()

    async def write_acquire(self):
        async with self._condition:
            self._writer_waiting += 1
            while self._state != LockState.IDLE:
                await self._condition.wait()
            self._writer_waiting -= 1
            self._state = LockState.WRITING

    async def write_release(self):
        async with self._condition:
            self._state = LockState.IDLE
            self._condition.notify_all()

async def reader(lock, id):
    await lock.read_acquire()
    print(f"Reader {id} acquired read lock")
    await asyncio.sleep(0.1)
    print(f"Reader {id} releasing read lock")
    await lock.read_release()

async def writer(lock, id):
    await lock.write_acquire()
    print(f"Writer {id} acquired write lock")
    await asyncio.sleep(0.2)
    print(f"Writer {id} releasing write lock")
    await lock.write_release()

async def main():
    lock = AsyncReadWriteLock()
    tasks = [
        reader(lock, 1),
        reader(lock, 2),
        writer(lock, 1),
        reader(lock, 3),
        writer(lock, 2),
        reader(lock, 4),
        reader(lock, 5),
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())