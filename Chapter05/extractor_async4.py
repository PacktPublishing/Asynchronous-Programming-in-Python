import asyncio
import aiohttp

BASE_URL = "https://ponyapi.net/v1/character/"

def get_data(person):
    try:
        p = person["data"][0]
        return f'{p["id"]}, {p["name"]}, {p["occupation"]}, {[k for k in p["kind"]]}'
    except (KeyError, IndexError) as e:  
        return f'Error processing data: {e}'
    except Exception as e:
        return f'Unexpected error: {e}'

async def fetch_person(session, url):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return f"Error: Status code {resp.status} for {url}" 
    except aiohttp.ClientError as e:  
        return f"Client error: {e} for {url}"
    except asyncio.TimeoutError:  
        return f"Timeout error for {url}"


async def get_people():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_person(session, BASE_URL + str(i)) for i in range(1, 200)] 

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results: 
            print(get_data(result) if isinstance(result, dict) else result) 

async def main():
    await get_people()

if __name__ == "__main__":
    asyncio.run(main())
