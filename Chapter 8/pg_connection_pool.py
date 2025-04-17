import time
import asyncio
import asyncpg

host="127.0.0.1"
user="postgres"
password="postgres"

async def bench_asyncpg_con():
    power = 2
    start = time.monotonic()
    for i in range(1, 1000):
        con = await asyncpg.connect(user=user, password=password, host=host)
        await con.fetchval('select 2 ^ $1', power)
        await con.close()

    end = time.monotonic()
    print(end - start, "Seconds for direct connection version")

async def bench_asyncpg_pool():
    pool = await asyncpg.create_pool(user=user, password=password, host=host)
    power = 2
    start = time.monotonic()
    for i in range(1, 1000):
        async with pool.acquire() as con:
            await con.fetchval('select 2 ^ $1', power)

    await pool.close()
    end = time.monotonic()
    print(end - start, "Seconds for pool version")

async def main():
    await bench_asyncpg_con()
    await bench_asyncpg_pool()

if __name__ == "__main__":
    asyncio.run(main())
