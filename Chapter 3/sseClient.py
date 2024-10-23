import json
import asyncio
from sseclient import SSEClient


messages = SSEClient('https://stream.wikimedia.org/v2/stream/recentchange')
batch_size = 3
vals = []

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
                    batch.append(change['user'])
                else: 
                    return batch                

async def fetcher():
    while True:
        io_vals = await sse_client_get_values()
        vals.extend(io_vals)
        await asyncio.sleep(1)

async def monitor():
    while True:
        print (len(vals))
        await asyncio.sleep(1)

async def main():
    t1 = asyncio.create_task(fetcher())
    t2 = asyncio.create_task(monitor())
    await asyncio.gather(t1, t2)

asyncio.run(main())