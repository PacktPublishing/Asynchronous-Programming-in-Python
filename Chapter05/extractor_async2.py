import asyncio
import aiohttp

BASE_URL = "https://ponyapi.net/v1/character/"

def get_data(person):
    try:
        p = person["data"][0]
        return f'{p["id"]}, {p["name"]}, {p["occupation"]}, {[k for k in p["kind"]]}'
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
        for i in range(1, 200):
            person_data = await get_data_nonblocking(session,BASE_URL + str(i))
            print(get_data(person_data))

async def main():
    await get_people()

if __name__ == "__main__":
    asyncio.run(main())
