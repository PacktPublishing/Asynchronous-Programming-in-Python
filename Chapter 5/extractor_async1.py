import time
import asyncio
import requests

BASE_URL = "https://ponyapi.net/v1/character/"

def get_data(person):
    try:
        p = person["data"][0]
        return f'{p["id"]}, {p["name"]}, {p["occupation"]}, {[k for k in p["kind"]]}'
    except Exception as e:
        return f'Error: {e}'


async def get_data_blocking(url):
    response = requests.get(url, timeout=30)
    if response.status_code == 200 and len(response.text) > 0:
        return response.json()
    else:
        return None

async def get_people():
    for i in range(1, 200):
        person_data = await get_data_blocking(BASE_URL + str(i))
        print(get_data(person_data))

async def main():
    await get_people()

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print('Time elapsed:',(end-start),'seconds')
