import trio
import json
import queue
import httpx
from httpx_sse import connect_sse

max_vals = 10
vals = queue.Queue(maxsize=max_vals)  
fetch_done = False

async def fetcher():
    while True:
        try:
            with httpx.Client() as client:
                with connect_sse(client, 'GET', 'https://stream.wikimedia.org/v2/stream/recentchange') as event_source:
                    for item in event_source.iter_sse():
                        vals.put(json.loads(item.data), block=False)
                        await trio.sleep(1)
        except queue.Full:
            print("Queue is full")
            return True
        
async def monitor():
    while True:
        curr_len = vals.qsize()
        if curr_len >= max_vals:
            fetch_done = True
            return True
        else:
            print("Queue size:",curr_len)
        await trio.sleep(1)
        
async def serializer():
    while True:
        try:
            item = vals.get_nowait()
            print("item read, Wiki edited by:", item["user"])
            f = trio.Path(f'./tmp/${item["id"]}.json')
            await f.write_text(json.dumps(item))
        except queue.Empty:
            print("Queue is empty")
            if fetch_done == True:
                return True
        await trio.sleep(1)

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(fetcher)
        nursery.start_soon(monitor)
        nursery.start_soon(serializer)

trio.run(main)