import asyncio
import aiohttp

BASE_URL = "http://api.nobelprize.org/2.0/laureate/"

def get_data(person):
    try:
        return f'{person[0]["id"]}, {person[0]["knownName"]["en"]}\, \
{[(n["awardYear"],n["category"]["en"]) for n in person[0]["nobelPrizes"]]}'
    except Exception as e:
        return f'Error: {e}'

async def get_data_nonblocking(session, url):
    try:
        async with session.get(url) as resp:
            results = await resp.json()
            return results
    except aiohttp.ClientResponseError as e:
        return str(e)

async def get_people():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 10):
            tasks.append(asyncio.ensure_future(get_data_nonblocking(session, BASE_URL + str(i))))

        results = await asyncio.gather(*tasks)
        for r in results:
            print(get_data(r))

async def main():
    await get_people()

if __name__ == "__main__":
    asyncio.run(main())
