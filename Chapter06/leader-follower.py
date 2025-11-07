import asyncio
import random

async def worker(queue, worker_id):
    while True:
        task = await queue.get()
        if task is None:
            queue.task_done() 
            break 
        print(f"Worker {worker_id} processing task: {task}")
        await asyncio.sleep(random.uniform(0.1, 0.5))  
        print(f"Worker {worker_id} finished task: {task}")
        queue.task_done()

async def leader(queue, num_tasks, num_workers):
    for i in range(num_tasks):
        task = f"Task {i + 1}"
        await queue.put(task)
        print(f"Leader added task: {task}")
        await asyncio.sleep(random.uniform(0.2, 0.8)) 
    
    for _ in range(num_workers):
        await queue.put(None)
    await queue.join() 

async def main():
    num_workers = 3
    num_tasks = 10
    queue = asyncio.Queue()
    workers = [asyncio.create_task(worker(queue, i)) for i in range(num_workers)]
    await leader(queue, num_tasks, num_workers)
    await asyncio.gather(*workers) 

if __name__ == "__main__":
    asyncio.run(main())