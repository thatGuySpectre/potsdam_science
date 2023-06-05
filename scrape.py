import aiohttp
import asyncio
from itertools import count
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


URL = "https://publishup.uni-potsdam.de/opus4-ubp/export/index/csv/searchtype/all/start/{}/rows/100/doctypefq/article"
QUEUE = count()
WORKERS = 100


async def scrape(session, num):
    async with session.get(
        url=URL.format(100 * num)
    ) as response:
        text = (await response.read()).decode("latin1")
        if text.count("\n") < 2:
            return False
        with open(f"data/{num:0>5}.csv", "w") as f:
            f.write(text)
        return True


async def worker(worker_id, session):
    running = True
    while running:
        num = QUEUE.__next__()
        if num % 1 == 0:
            logger.info(f"writing {num}")
        running = await scrape(session, num)
        if not running:
            logger.info(f"worker {worker_id} got nil on {num}, quitting")


async def main():
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(worker(i, session)) for i in range(WORKERS)
        ]
        for w in workers:
            await w


if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())