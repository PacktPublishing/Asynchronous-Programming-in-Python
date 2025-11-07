import asyncio
import csv
import sqlite3
import aiosqlite

async def create_table(db_path, table_name, column_names):
    async with aiosqlite.connect(db_path) as db:
        columns_str = ", ".join(f"{col} TEXT" for col in column_names)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        await db.execute(create_table_sql)
        await db.commit()
    print(f"Table '{table_name}' created (or already existed).")

async def insert_data(db_path, table_name, data):
    try:
        async with aiosqlite.connect(db_path) as db:
            columns = ", ".join(data.keys())
            placeholders = ", ".join("?" * len(data))
            values = tuple(data.values())
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            await db.execute(insert_sql, values)
            await db.commit()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked for writing...")
        else:
            raise e

async def process_csv_and_insert(db_path, table_name, csv_file_path):
    data_list = []
    column_names = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        column_names = reader.fieldnames
        for row in reader:
            data_list.append(row)

    await create_table(db_path, table_name, column_names)
    tasks = [insert_data(db_path, table_name, data) for data in data_list]
    await asyncio.gather(*tasks)

async def main():
    db_path = "async.sqlite"
    table_name = "async_filled"
    csv_file_path = "fine_food_reviews_with_embeddings_1k.csv"
    await process_csv_and_insert(db_path, table_name, csv_file_path)

if __name__ == "__main__":
    asyncio.run(main())
