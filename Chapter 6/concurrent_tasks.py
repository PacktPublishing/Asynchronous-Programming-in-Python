import time
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

async def print_document(doc_name, sleep_time):
    print(f"[{time.strftime('%X')}] Print '{doc_name}'...")
    await asyncio.sleep(sleep_time)
    print(f"[{time.strftime('%X')}] Finished.")

async def main():
    doc1 = print_document("Report.pdf", 3)
    doc2 = print_document("Presentation.pptx", 1)
    doc3 = print_document("Brochure.docx", 2)
    await asyncio.gather(get_nobel_name(659), doc1, doc2, doc3)
    
if __name__ == "__main__":
    asyncio.run(main())