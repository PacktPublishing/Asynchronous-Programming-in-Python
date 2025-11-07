import json
import queue
import asyncio
from sseclient import SSEClient


messages = SSEClient('https://stream.wikimedia.org/v2/stream/recentchange')
batch_size = 3
max_vals = 10
vals = queue.Queue(maxsize=max_vals)

async def sse_client_get_values():
    batch = []
    for event in messages:
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                if change['meta']['domain'] == 'canary' or change['bot'] == True:
                    continue            
                if len(batch) < batch_size:
                    batch.append(change)
                else: 
                    return batch                

async def fetcher():
    while True:
        io_vals = await sse_client_get_values()
        try:
            for item in io_vals:
        	    vals.put(item, block=False)
        except queue.Full:
            print("Queue is full")
            return True
        await asyncio.sleep(1)
        
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