import asyncio
import concurrent.futures

async def cpu_bound_task(x):
    await asyncio.sleep(1)
    return x * x

def run_cpu_bound_task(x):
    return asyncio.run(cpu_bound_task(x))

async def main():
    with concurrent.futures.ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(pool, run_cpu_bound_task, i)
            for i in range(5)
        ]
        results = await asyncio.gather(*tasks)
        print(results)

if __name__ == "__main__":
    asyncio.run(main())