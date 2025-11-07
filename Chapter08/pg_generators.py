import asyncio
import asyncpg

host="127.0.0.1"
user="postgres"
password="postgres"

async def create_connection_pool():
    try:
        pool = await asyncpg.create_pool(user=user,password=password,host=host)
        return pool
    except Exception as e:
        print(f"Error creating connection pool: {e}")
        raise

async def generate_rows(pool, table_name):
    async with pool.acquire() as conn:
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY,
                name TEXT,
                value INTEGER)""")
        await conn.execute(f"TRUNCATE TABLE {table_name}")
        await conn.executemany(
            f"INSERT INTO {table_name} (name, value) VALUES ($1, $2)",
            [(f"row {i}",i) for i in range(1,100000)]
        )

async def fetch_all_in_memory(pool, table_name):
    try:
        async with pool.acquire() as conn:
            query = f"SELECT * FROM {table_name}"
            rows = await conn.fetch(query)
            print(f"Fetched {len(rows)} rows into memory.")
            return [tuple(row) for row in rows]
    except Exception as e:
        print(f"Error fetching all data in memory: {e}")
        return []


async def fetch_in_pages(pool, table_name, page_size = 10000):
    all_rows = []
    offset = 0
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                cursor = await conn.cursor(f"SELECT * FROM {table_name}")
                while True:
                    rows = await cursor.fetch(page_size)
                    if len(rows) < 1:
                        break
                    all_rows.extend([tuple(row) for row in rows])
                    print(f"Fetched page {(offset/page_size)+1}")
                    offset += page_size
                print(f"Fetched {len(all_rows)} rows using pagination.")
                return all_rows
    except Exception as e:
        print(f"Error fetching data with pagination: {e}")
        return []


async def fetch_as_generator(pool, table_name):
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                query = f"SELECT * FROM {table_name}"
                async for row in conn.cursor(query):
                    yield tuple(row)
        print(f"Generator created for fetching rows from {table_name}")
    except Exception as e:
        print(f"Error creating generator: {e}")
        yield None

async def main():
    pool = await create_connection_pool()
    table_name = "sample_table"
    await generate_rows(pool, table_name)
    all_rows = await fetch_all_in_memory(pool, table_name)
    paged_rows = await fetch_in_pages(pool, table_name)
    total_rows = 0
    async for row in fetch_as_generator(pool, table_name):
        total_rows+=1
    print(f"Rows fetched from generator: {total_rows}")
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())