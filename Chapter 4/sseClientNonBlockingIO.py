import json
import queue
import asyncio
from aiosseclient import aiosseclient

max_vals = 10
vals = queue.Queue(maxsize=max_vals)  

async def fetcher():
    while True:
        try:
            async for item in aiosseclient('https://stream.wikimedia.org/v2/stream/recentchange'):
                vals.put(item, block=False)
                await asyncio.sleep(1)
        except queue.Full:
            print("Queue is full")
            return True
        
async def monitor():
    while True:
        curr_len = vals.qsize()
        if curr_len >= max_vals:
            return True
        else:
            print("Queue size:",curr_len)
        await asyncio.sleep(1)
        
async def serializer():
    while True:
        try:
            item = vals.get_nowait()
            print("item read, Wiki edited by:", item["user"])
            f = open(f'./tmp/${item["id"]}.json', "a")
            json.dump(item, f)
            f.close()
        except queue.Empty:
            print("Queue is empty")
            return True
        await asyncio.sleep(1)
        
async def main():
    t1 = asyncio.create_task(fetcher())
    t2 = asyncio.create_task(monitor())
    t3 = asyncio.create_task(serializer())
    await asyncio.gather(t1, t2, t3)

asyncio.run(main())