import asyncio
import queue
import random

class MonitorQueue:
    def __init__(self, maxsize=3):
        self._queue = queue.Queue(maxsize=maxsize)
        self._lock = asyncio.Lock()
        self._not_empty = asyncio.Condition(self._lock)
        self._not_full = asyncio.Condition(self._lock)

    async def enqueue(self, item):
        async with self._lock:
            while self._queue.full():
                await self._not_full.wait()
            self._queue.put(item)
            self._not_empty.notify_all()
            print(f"Enqueued: {item}, size: {self._queue.qsize()}")

    async def dequeue(self):
        async with self._lock:
            while self._queue.empty():
                await self._not_empty.wait()
            item = self._queue.get()
            self._not_full.notify_all()
            print(f"Dequeued: {item}")
            return item

async def producer(monitor_queue, producer_id):
    for i in range(10):
        item = f"Producer {producer_id} - Item {i}"
        await monitor_queue.enqueue(item)
        await asyncio.sleep(random.random() * 0.5)

async def consumer(monitor_queue, consumer_id):
    while True:
        item = await monitor_queue.dequeue()
        print(f"Consumer - {consumer_id} - Got {item}")
        await asyncio.sleep(random.random() * 1)

async def main():
    monitor_queue = MonitorQueue()

    producer1 = asyncio.create_task(producer(monitor_queue, 1))
    producer2 = asyncio.create_task(producer(monitor_queue, 2))
    consumer1 = asyncio.create_task(consumer(monitor_queue, 1))
    consumer2 = asyncio.create_task(consumer(monitor_queue, 2))

    await asyncio.gather(producer1, producer2)
    await asyncio.sleep(5)
    consumer1.cancel()
    consumer2.cancel()

    try:
        await consumer1
    except asyncio.CancelledError:
        print("Consumer 1 cancelled")
    try:
        await consumer2
    except asyncio.CancelledError:
        print("Consumer 2 cancelled")

if __name__ == "__main__":
    asyncio.run(main())