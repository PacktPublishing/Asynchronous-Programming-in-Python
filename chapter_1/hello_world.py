import asyncio


async def print_range(iterable, interval=0.1):
    for i in iterable:
        print(i)
        await asyncio.sleep(interval)


async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(print_range(range(0, 5)))
        task2 = tg.create_task(print_range(range(10, 15)))


asyncio.run(main())

