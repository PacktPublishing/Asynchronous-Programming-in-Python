import csv
import asyncio
import lancedb
import pyarrow as pa

async def create_table(db_path, table_name):
    schema = pa.schema(
        [
            pa.field("Id", pa.string()),
            pa.field("ProductId", pa.string()),
            pa.field("UserId", pa.string()),
            pa.field("Score", pa.string()),
            pa.field("Summary", pa.string()),
            pa.field("Text", pa.string()),
            pa.field("combined", pa.string()),
            pa.field("n_tokens", pa.string()),
            pa.field("embedding", pa.string())
        ]
    )
    db =  await lancedb.connect_async(db_path)
    await db.create_table(table_name, schema=schema, mode="overwrite")

    print(f"Table '{table_name}' created (or already existed).")

async def insert_data(db_path, table_name, data):
    try:
        db = await lancedb.connect_async(db_path)
        async_tbl = await db.open_table(table_name)
        await async_tbl.add([data])
    except Exception as e:
        print(f"Error writing into database...{e}")

async def process_csv_and_insert(db_path, table_name, csv_file_path):
    data_list = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append(row)

    await create_table(db_path, table_name)
    tasks = [insert_data(db_path, table_name, data) for data in data_list]
    await asyncio.gather(*tasks)

async def main():
    db_path = "tmp/async_lancedb"
    table_name = "async_filled"
    csv_file_path = "fine_food_reviews_with_embeddings_1k.csv"
    await process_csv_and_insert(db_path, table_name, csv_file_path)

if __name__ == "__main__":
    asyncio.run(main())
