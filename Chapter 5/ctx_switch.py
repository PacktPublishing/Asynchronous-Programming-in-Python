import asyncio

async def simplistic():
    await asyncio.sleep(0.000001)

async def main():
    tasks = [simplistic() for i in range(1,100000)]
    await asyncio.gather(*(tasks))

asyncio.run(main())