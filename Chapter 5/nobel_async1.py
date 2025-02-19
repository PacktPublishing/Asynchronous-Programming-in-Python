import asyncio
import requests

BASE_URL = "http://api.nobelprize.org/2.1/laureate/"

def get_data(person):
    try:
        return f'{person[0]["id"]}, {person[0]["knownName"]["en"]}\, \
{[(n["awardYear"],n["category"]["en"]) for n in person[0]["nobelPrizes"]]}'
    except Exception as e:
        return f'Error: {e}'


def get_data_blocking(url):
    response = requests.get(url, timeout=30)
    if response.status_code == 200 and len(response.text) > 0:
        return response.json()
    else:
        return None

def get_people():
    for i in range(1, 10):
        person_data = get_data_blocking(BASE_URL + str(i))
        print(get_data(person_data))

async def main():
    get_people()

if __name__ == "__main__":
    asyncio.run(main())
