import asyncio
import aiohttp

URL="https://api.nobelprize.org/2.1/laureate/"

async def get_nobel_name(nid):
    print("Starting nobel extraction")
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL+str(nid)) as response:
            if response.status == 200:
                nobel = await response.json()
                print(len(nobel)," Nobel found!")
                return(nobel[0]["knownName"]["en"])

async def get_odds(max_num):
    print("Starting get_odds")
    res = []
    for num in range(0,max_num):
        r = (num % 2 != 0)
        res.append(r)
        print(f"{num} is odd? {r}")
        await asyncio.sleep(1)
    return(res)

async def main():
    await asyncio.gather(get_nobel_name(659), get_odds(10))
    
if __name__ == "__main__":
    asyncio.run(main())