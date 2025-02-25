import queue
import asyncio
import logging
from logging.handlers import QueueHandler, QueueListener
import aiohttp

log_queue = queue.Queue()
queue_handler = QueueHandler(log_queue)
listener = QueueListener(log_queue, *logging.root.handlers)
logging.root.addHandler(queue_handler)
listener.start()
logger = logging.getLogger(__name__)
BASE_URL = "https://ponyapi.net/v1/character/"

def print_data(person):
    try:
        p = person["data"][0]
        print(f'{p["id"]}, {p["name"]}, {p["occupation"]}, {[k for k in p["kind"]]}')
    except (KeyError, IndexError) as e:
        logger.error('Error processing data: %s',e)
    except Exception as e:
        logger.error('Unexpected error: %s',e)

async def fetch_person(session, url):
    try:
        async with session.get(url) as resp:
            return await resp.json() if resp.status == 200 else f"Error in HTTP client for {url}"
    except aiohttp.ClientError as e:
        logger.error("Client error: %s for %s", e, url)
    except asyncio.TimeoutError:
        logger.error("Timeout error for %s", e)
    return None

async def get_people():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_person(session, BASE_URL + str(i)) for i in range(1, 200)] 

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, dict):
                print_data(result)

async def main():
    await get_people()

if __name__ == "__main__":
    asyncio.run(main())
    listener.stop()
    logging.root.removeHandler(queue_handler)